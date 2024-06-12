package com.jmdm.squiz.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.jmdm.squiz.enums.SubjectType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@Schema(description = "과일 바구니 관련 정보")
public class FruitBasketDTO {
    @Schema(description = "db에 저장되는 과일 바구니 id", defaultValue = "1")
    private Long fruitBasketId;
    @Schema(description = "과일바구니 이름", defaultValue = "과일바구니 이름")
    private String fruitBasketName;
    @Schema(description = "과목", defaultValue = "OPERATING_SYSTEM")
    private SubjectType subjectType;
    @Schema(description = "문제 수", defaultValue = "15")
    private int problemNum;

    @Schema(description = "생성 일")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss", timezone = "Asia/Seoul")
    private LocalDateTime createdAt;
    @Schema(description = "수정 일")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss", timezone = "Asia/Seoul")
    private LocalDateTime updatedAt;

    @Builder
    public FruitBasketDTO(Long fruitBasketId, String fruitBasketName, SubjectType subjectType, int problemNum, LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.fruitBasketId = fruitBasketId;
        this.fruitBasketName = fruitBasketName;
        this.subjectType = subjectType;
        this.problemNum = problemNum;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }
}
