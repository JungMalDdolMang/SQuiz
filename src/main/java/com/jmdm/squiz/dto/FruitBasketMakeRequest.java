package com.jmdm.squiz.dto;

import com.jmdm.squiz.enums.SubjectType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "과일 바구니 생성 request")
public class FruitBasketMakeRequest {
    @Schema(description = "과목", defaultValue = "OPERATING_SYSTEM")
    private SubjectType subjectType;
    @Schema(description = "과일바구니 이름", defaultValue = "과일바구니 이름")
    private String fruitBasketName;

}
