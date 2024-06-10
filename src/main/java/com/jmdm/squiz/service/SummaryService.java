package com.jmdm.squiz.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jmdm.squiz.domain.Member;
import com.jmdm.squiz.domain.Pdf;
import com.jmdm.squiz.domain.Quiz;
import com.jmdm.squiz.domain.Summary;
import com.jmdm.squiz.dto.AiQuizGenerateResponse;
import com.jmdm.squiz.dto.AiSummaryGenerateResponse;
import com.jmdm.squiz.dto.SummaryGenerateResponse;
import com.jmdm.squiz.exception.ErrorCode;
import com.jmdm.squiz.exception.model.AiServerException;
import com.jmdm.squiz.exception.model.NotFoundPdfException;
import com.jmdm.squiz.exception.model.NotFoundQuizException;
import com.jmdm.squiz.repository.MemberRepository;
import com.jmdm.squiz.repository.PdfRepository;
import com.jmdm.squiz.repository.QuizRepository;
import com.jmdm.squiz.repository.SummaryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class SummaryService {
    private final PdfRepository pdfRepository;
    private final MemberRepository memberRepository;
    private final SummaryRepository summaryRepository;
    private final QuizRepository quizRepository;
    private final FileService fileService;
    @Value("${ai.server.url}")
    private String aiUrl;

    public SummaryGenerateResponse loadSummary(Long quizId) throws IOException {
        Quiz quiz = quizRepository.findById(quizId)
                .orElseThrow(() -> new NotFoundQuizException(ErrorCode.QUIZ_NOT_FOUND, ErrorCode.QUIZ_NOT_FOUND.getMessage()));
        Summary summary = summaryRepository.findByPdf(quiz.getPdf());
        SummaryGenerateResponse response = new SummaryGenerateResponse();
        response.setSummary(fileService.loadDataFromUrl(summary.getFilePath()));
        return response;
    }

    public SummaryGenerateResponse generateSummary(String memberId, Long pdfId) throws IOException {
        Pdf pdf = pdfRepository.findById(pdfId)
                .orElseThrow(() -> new NotFoundPdfException(ErrorCode.PDF_NOT_FOUND, ErrorCode.PDF_NOT_FOUND.getMessage()));
        Member member = memberRepository.findByMemberId(memberId);

        AiSummaryGenerateResponse aiResponse = postAiAndGetSummary(pdf);
        String storedFileName = fileService.getStoredFileName(".md");
        String s3FilePath = fileService.saveData(aiResponse.getSummaryInMd(), storedFileName);
        Summary summary = Summary.builder()
                .storedFileName(storedFileName)
                .filePath(s3FilePath)
                .pdf(pdf)
                .build();
        summaryRepository.save(summary);
        SummaryGenerateResponse response = new SummaryGenerateResponse();
        response.setSummary(aiResponse.getSummaryInMd());
        return response;
    }

    private AiSummaryGenerateResponse postAiAndGetSummary(Pdf pdf) throws IOException {
        // post 요청할 ai 서버 url
        String aiServerUrl = aiUrl + "/summary";
        // 요청 header 설정
        HttpHeaders headers = new org.springframework.http.HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 요청 body 설정
        Map<String, Object> body = new HashMap<>();
        body.put("pdfId", pdf.getId());
        body.put("pdfText", fileService.loadDataFromUrl(pdf.getFilePath()));
        body.put("subject", pdf.getSubjectType());
        body.put("pageKcId", fileService.loadDataFromUrl(pdf.getKcDataFilePath()));
        System.out.println("body = " + body);

        // post 요청
        RestTemplate restTemplate = new RestTemplate();
        HttpEntity<Map<String, Object>> AiRequest = new HttpEntity<>(body, headers);
        ResponseEntity<String> AiResponse = restTemplate.postForEntity(aiServerUrl, AiRequest, String.class);

        // problem, answer 저장
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(AiResponse.getBody(), AiSummaryGenerateResponse.class);
    }

}
