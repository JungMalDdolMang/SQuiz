package com.jmdm.squiz.service;

import com.jmdm.squiz.domain.*;
import com.jmdm.squiz.dto.QuizDTO;
import com.jmdm.squiz.dto.QuizListLoadResponse;
import com.jmdm.squiz.enums.KC;
import com.jmdm.squiz.repository.DktPerSubjectRepository;
import com.jmdm.squiz.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;


@Service
@RequiredArgsConstructor
public class QuizListLoadService {
    private final MemberRepository memberRepository;
    private final DktPerSubjectRepository dktPerSubjectRepository;

    private static final float CRITERIA = 50;
    public QuizListLoadResponse loadQuizList(String memberId) {
        Member member = memberRepository.findByMemberId(memberId);
        List<Quiz> quizList = member.getQuizs();
        ArrayList<QuizDTO> quizDTOArrayList = new ArrayList<>();
        for (Quiz quiz : quizList) {
            QuizDTO dto = QuizDTO.builder()
                    .quizId(quiz.getId())
                    .quizName(quiz.getQuizName())
                    .subjectType(quiz.getSubject())
                    .problemNum(quiz.getProblemNum())
                    .correctNum(quiz.getCorrectNum())
                    .createdAt(quiz.getCreatedAt())
                    .uploadFileName(quiz.getPdf().getUploadFileName())
                    .weakPart(getWeakPart(member, quiz))
                    .build();
            quizDTOArrayList.add(dto);
        }
        QuizListLoadResponse response = new QuizListLoadResponse();
        response.setQuizList(quizDTOArrayList);
        return response;
    }

    private ArrayList<String> getWeakPart(Member member, Quiz quiz) {
        ArrayList<String> weakPart = new ArrayList<>();
        HashSet<Integer> kcIdList = new HashSet<>();
        List<Problem> problems = quiz.getProblems();
        for (Problem problem : problems) {
            kcIdList.add(problem.getKcId());
        }
        DktPerSubject dktPerSubject = dktPerSubjectRepository.findByMemberAndSubjectType(member, quiz.getSubject());
        List<DktList> dktLists = dktPerSubject.getDktLists();

        kcIdList.forEach(targetKcId -> {
            List<DktList> targetDktLists = dktLists.stream()
                .filter(dkt -> dkt.getKcId() == targetKcId)
                .toList();
             for (DktList dkt : targetDktLists) {
                 if (dkt.getPredict() < CRITERIA) {
                     weakPart.add(KC.fromId(dkt.getKcId()));
                 }
             }
        });
        return weakPart;
    }
}
