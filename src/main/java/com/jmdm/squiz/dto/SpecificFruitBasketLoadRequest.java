package com.jmdm.squiz.dto;

import com.jmdm.squiz.enums.SubjectType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "특정 과목 과일바구니 목록 로드 request")
public class SpecificFruitBasketLoadRequest {
    @Schema(description = "과목명", defaultValue = "OPERATING_SYSTEM")
    private SubjectType subjectType;
}
