package com.jmdm.squiz.dto;

import com.jmdm.squiz.enums.ProblemNum;
import com.jmdm.squiz.enums.QuizType;
import com.jmdm.squiz.enums.Rank;
import com.jmdm.squiz.enums.SubjectType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import javax.validation.constraints.NotBlank;

@Data
@Schema(description = "퀴즈 생성 시 요청하는 request")
public class QuizGenerateRequest {
    @NotBlank()
    @Schema(description = "생성하려는 퀴즈의 pdfId(Long 타입)", nullable = false,
    defaultValue = "1")
    private Long pdfId;

    @Schema(description = "사용자가 설정한 퀴즈 이름", defaultValue = "퀴즈 이름")
    @NotBlank(message = "퀴즈 이름은 필수입니다.")
    private String quizName;

    @NotBlank(message = "과목 선택은 필수입니다.")
    @Schema(description = "과목 유형",
            defaultValue = "OPERATING_SYSTEM")
    private SubjectType subjectType;

    @NotBlank(message = "시작 페이지는 필수입니다.")
    @Schema(description = "시작 페이지 1 이상", defaultValue = "1")
    private int startPage;

    @NotBlank(message = "끝 페이지는 필수입니다.")
    @Schema(description = "끝 페이지",
    defaultValue = "2")
    private int endPage;

    @NotBlank(message = "문제 유형은  필수입니다.")
    @Schema(description = "퀴즈 유형",
            defaultValue = "MULTIPLE_CHOICE")
    private QuizType quizType;

    @NotBlank(message = "문제 개수는 필수입니다.")
    @Schema(description = "문제 개수",
    allowableValues = {"5", "10", "15", "20"},
    defaultValue = "5")
    private int problemNum;

    @NotBlank(message = "난이도는 필수입니다.")
    @Schema(description = "문제 난이도",
    defaultValue = "MIDDLE")
    private Rank rank;
}
