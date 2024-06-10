package com.jmdm.squiz.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "문제 객체")
public class ProblemDTO {
    @Schema(description = "문제 번호",
            defaultValue = "1")
    private int problemNo;
    @Schema(description = "문제",
            defaultValue = "올바른 선택지를 고르시오.")
    private String question;
    @Schema(description = "선택지 만약 객관식이 아니라면 각 값은 null")
    private Options options;
    @Schema(description = "빈칸이 포함된 내용 만약 빈칸이 아니라면 null",
            defaultValue = "null")
    private String content;
    @Schema(description = "빈칸 수", defaultValue = "1")
    private int blankNum;
}

