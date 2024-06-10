package com.jmdm.squiz.dto;

import com.jmdm.squiz.enums.SubjectType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import java.util.ArrayList;
import java.util.List;

@Data
@Schema(description = "퀴즈 채점 결과")
public class QuizCheckResponse {
    @Schema(description = "db에 저장되는 quizId",
            defaultValue = "1")
    private Long quizId;

    @Schema(description = "db에 저장되는 pdfId", defaultValue = "1")
    private Long pdfId;

    @Schema(description = "db에 저장되는 summaryId, null이면 요약본 생성하기 다른 값이 있으면 요약본 로드 하기",
    defaultValue = "null")
    private Long summaryId;

    @Schema(description = "퀴즈 이름",
    defaultValue = "운영체제 1강")
    private String quizName;

    @Schema(description = "문제 개수",
    allowableValues = {"5", "10", "15", "20"},
    defaultValue = "15")
    private int problemNum;

    @Schema(description = "맞은 개수",
    defaultValue = "10")
    private int correctNum;

    @Schema(description = "과목", defaultValue = "OPERATING_SYSTEM")
    private SubjectType subject;

    @Schema(description = "페이지 수", defaultValue = "20")
    private int totalPageNum;

    @Schema(description = "업로드한 파일이름", defaultValue = "운영체제 5장.pdf")
    private String uploadFileName;

    @Schema(description = "해당 pdf로 요청한 퀴즈 수", defaultValue = "1")
    private int generatedQuizNum;

    @Schema(description = "kc 마다의 총 개수와 맞은 개수")
    private List<CorrectPerKcDTO> correctPerKcDTOS;
}

