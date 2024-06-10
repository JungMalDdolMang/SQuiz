package com.jmdm.squiz.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.jmdm.squiz.domain.*;
import com.jmdm.squiz.dto.*;
import com.jmdm.squiz.enums.QuizType;
import com.jmdm.squiz.enums.SubjectType;
import com.jmdm.squiz.exception.ErrorCode;
import com.jmdm.squiz.exception.model.AiServerException;
import com.jmdm.squiz.exception.model.NotFoundPdfException;
import com.jmdm.squiz.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class QuizGenerateService {
    private final MemberRepository memberRepository;
    private final PdfRepository pdfRepository;
    private final QuizRepository quizRepository;
    private final ProblemRepository problemRepository;
    private final DktPerSubjectRepository dktPerSubjectRepository;
    private final FileService fileService;
    @Value("${ai.server.url}")
    private String aiUrl;
    @Transactional
    public QuizGenerateResponse generateQuiz(String memberId, QuizGenerateRequest request) throws IOException {
        // pdf 파일 load
        Long pdfId =request.getPdfId();
        Pdf pdf = pdfRepository.findById(pdfId)
                .orElseThrow(() -> new NotFoundPdfException(ErrorCode.PDF_NOT_FOUND, ErrorCode.PDF_NOT_FOUND.getMessage()));

        // member load
        Member member = memberRepository.findByMemberId(memberId);

        // quiz 저장
        Quiz quiz = saveQuizAndGetQuiz(pdf, member, request);

        //post
        ArrayList<Dkt> dkts = isPlusQuiz(member, quiz.getSubject());
        AiQuizGenerateResponse AiResponse = postAiAndGetQuiz(quiz.getId(), pdf, request, dkts); // ai post api 호출
//        AiQuizGenerateResponse AiResponse = aiTest(quiz.getId(), request);
        System.out.println("AiResponse = " + AiResponse);
        saveProblem(AiResponse, quiz);
        return makeResponse(AiResponse, request);
    }

    private QuizGenerateResponse makeResponse(AiQuizGenerateResponse aiResponse, QuizGenerateRequest request) {
        QuizGenerateResponse response = new QuizGenerateResponse();
        response.setQuizId(aiResponse.getQuizId());
        response.setQuizType(aiResponse.getQuizType());
        response.setQuizName(request.getQuizName());
        response.setProblemNum(request.getProblemNum());
        ArrayList<ProblemDTO> problemDTOS = new ArrayList<>();
        for (AiProblemDTO aiProblemDTO : aiResponse.getProblemList()) {
            ProblemDTO problemDTO = new ProblemDTO();
            problemDTO.setProblemNo(aiProblemDTO.getProblemNo());
            problemDTO.setQuestion(aiProblemDTO.getQuestion());
            problemDTO.setOptions(aiProblemDTO.getOptions());
            problemDTO.setContent(aiProblemDTO.getContent());
            if (response.getQuizType().equals(QuizType.BLANK)) {
                problemDTO.setBlankNum(4 - getBlankNum(aiProblemDTO));
            }
            problemDTOS.add(problemDTO);

        }
        response.setProblemList(problemDTOS);
        return response;
    }
    private int getBlankNum(AiProblemDTO aiProblemDTO) {
    Blanks blanks = aiProblemDTO.getBlanks();
    int count = 0;

    if (blanks != null) {
        if ("none".equals(blanks.getBlank_1())) {
            count++;
        }
        if ("none".equals(blanks.getBlank_2())) {
            count++;
        }
        if ("none".equals(blanks.getBlank_3())) {
            count++;
        }
        if ("none".equals(blanks.getBlank_4())) {
            count++;
        }
    }

    return count;
}

    private Quiz saveQuizAndGetQuiz(Pdf pdf, Member member, QuizGenerateRequest request) {
//        System.out.println(pdf);
//        System.out.println(member);
//        System.out.println(request);
        Quiz quiz = Quiz.builder()
                .pdf(pdf)
                .member(member)
                .quizName(request.getQuizName())
                .subject(request.getSubject())
                .startPage(request.getStartPage())
                .endPage(request.getEndPage())
                .quizType(request.getQuizType())
                .problemNum(request.getProblemNum())
                .rank(request.getRank())
                .build();
        quizRepository.save(quiz);
        return quiz;
    }

    private ArrayList<Dkt> isPlusQuiz(Member member, SubjectType subjectType) {
        if (dktPerSubjectRepository.existsByMemberAndSubjectType(member, subjectType)) {
            DktPerSubject dktPerSubject = dktPerSubjectRepository.findByMemberAndSubjectType(member,subjectType);
            List<DktList> dktLists = dktPerSubject.getDktLists();

            return dktLists.stream()
                    .map(dktList -> {
                        Dkt dkt = new Dkt();
                        dkt.setKcId(dktList.getKcId());
                        dkt.setPredict(dktList.getPredict());
                        return dkt;
                    })
                    .collect(Collectors.toCollection(ArrayList::new));
        } else {
            return null;
        }
    }


    private AiQuizGenerateResponse postAiAndGetQuiz(Long quizId, Pdf pdf, QuizGenerateRequest request, ArrayList<Dkt> dkts) throws IOException{
        // post 요청할 ai 서버 url
        String aiServerUrl = aiUrl + "/quiz";
        // 요청 header 설정
        HttpHeaders headers = new org.springframework.http.HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 요청 body 설정
        Map<String, Object> body = new HashMap<>();
        body.put("quizId", quizId);
        body.put("subject", pdf.getSubjectType().toString());
        body.put("startPage", request.getStartPage());
        body.put("endPage", request.getEndPage());
        body.put("quizType", request.getQuizType());
        body.put("problemNum", request.getProblemNum());
        body.put("rank", request.getRank());
        body.put("pdfText", fileService.loadDataFromUrl(pdf.getFilePath()));
        body.put("pageKcId", fileService.loadDataFromUrl(pdf.getKcDataFilePath()));
        body.put("dkt", dkts); // 추후 문제 재생성시로 바꾸기
        System.out.println("body = " + body);

        // post 요청
        RestTemplate restTemplate = new RestTemplate();
        HttpEntity<Map<String, Object>> AiRequest = new HttpEntity<>(body, headers);
        ResponseEntity<String> AiResponse = restTemplate.postForEntity(aiServerUrl, AiRequest, String.class);

        // problem, answer 저장
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(AiResponse.getBody(), AiQuizGenerateResponse.class);
    }

    private void saveProblem(AiQuizGenerateResponse response, Quiz quiz) {
        ArrayList<AiProblemDTO> aiProblemDTOS = response.getProblemList();

        for (AiProblemDTO aiProblemDTO : aiProblemDTOS) {
            Problem problem = Problem.builder()
                    .quiz(quiz)
                    .kcId(aiProblemDTO.getKcId())
                    .problemNo(aiProblemDTO.getProblemNo())
                    .question(aiProblemDTO.getQuestion())
                    .options(aiProblemDTO.getOptions())
                    .content(aiProblemDTO.getContent())
                    .blanks(aiProblemDTO.getBlanks())
                    .answer(aiProblemDTO.getAnswer())
                    .explanation(aiProblemDTO.getExplanation())
                    .build();
            problemRepository.save(problem);
        }
    }



}
