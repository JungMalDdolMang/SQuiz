package com.jmdm.squiz.controller;

import com.jmdm.squiz.dto.*;
import com.jmdm.squiz.exception.SuccessCode;
import com.jmdm.squiz.service.FruitBasketService;
import com.jmdm.squiz.utils.ApiResponseEntity;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/fruit-basket")
@Tag(name = "과일바구니 API", description = "과일바구니를 불러오고 각 바구니의 문제를 제공하는 API입니다.")
public class FruitBasketController {
    private final FruitBasketService fruitBasketService;

    @GetMapping("/load")
    @Operation(summary = "과일 바구니 목록을 불러오는 API",
            description = "사용자의 모든 과일바구니를 제공하는 API입니다.")
    @ApiResponse(responseCode = "200", description = "사용자의 과일 바구니 로드 성공", content = @Content(schema = @Schema(implementation = FruitBasketsLoadResponse.class)))
    public ResponseEntity<ApiResponseEntity<FruitBasketsLoadResponse>> loadFruitBaskets(@AuthenticationPrincipal CustomUserDetails userDetails) {
        System.out.println("\n\n Get /api/v1/fruit-basket/load 호출 \n\n");
        System.out.println("userDetails = " + userDetails);
        String memberId = userDetails.getUsername();
        FruitBasketsLoadResponse response = fruitBasketService.loadFruitBasket(memberId);
        System.out.println("\n\n Get /api/v1/fruit-basket/load 호출 완료 \n\n");
        System.out.println("response = " + response);
        return ResponseEntity.ok(ApiResponseEntity.ok(SuccessCode.SUCCESS, response, "과일 바구니 목록입니다."));
    }

    @PostMapping("/make")
    @Operation(summary = "과일 바구니를 만드는 API",
    description = "문제를 풀고 난 후 과일바구니를 선택하는 상황에서 새로운 과일바구니를 만들었을 때 사용하는 API")
    @ApiResponse(responseCode = "200", description = "새로운 과일바구니 생성 성공", content = @Content(schema = @Schema(implementation = FruitBasketMakeResponse.class)))
    public ResponseEntity<ApiResponseEntity<FruitBasketMakeResponse>> makeFruitBasket(@AuthenticationPrincipal CustomUserDetails userDetails,
                                                                                      @RequestBody FruitBasketMakeRequest request) {
        System.out.println("\n\n Post /api/v1/fruit-basket/make 호출 \n\n");
        System.out.println("userDetails = " + userDetails + ", request = " + request);
        String memberId = userDetails.getUsername();
        FruitBasketMakeResponse response = fruitBasketService.makeFruitBasket(memberId, request);
        System.out.println("\n\n Post /api/v1/fruit-basket/make 호출 완료 \n\n");
        System.out.println("response = " + response);
        return ResponseEntity.ok(ApiResponseEntity.ok(SuccessCode.SUCCESS, response, "새로 만들어진 과일바구니 id"));
    }

    @PostMapping("/load-specific")
    @Operation(summary = "특정 과목의 과일바구니 목록을 불러오는 API",
    description = "문제를 풀고 별표를 눌렀을때 과일바구니 목록들 요청시 사용하는 API")
    @ApiResponse(responseCode = "200", description = "특정 과목 과일바구니 목록 로드 성공", content = @Content(schema = @Schema(implementation = SpecificFruitBasketsLoadResponse.class)))
    public ResponseEntity<ApiResponseEntity<SpecificFruitBasketsLoadResponse>> loadSpecificFruitBaskets(@AuthenticationPrincipal CustomUserDetails userDetails,
                                                                                                        @RequestBody SpecificFruitBasketLoadRequest request) {
        String memberId = userDetails.getUsername();
        System.out.println("\n\n Post /api/v1/fruit-basket/load-specific 호출 \n\n");
        System.out.println("userDetails = " + userDetails + ", request = " + request);
        SpecificFruitBasketsLoadResponse response = fruitBasketService.loadSpecificFruitBaskets(memberId, request);
        System.out.println("\n\n Post /api/v1/fruit-basket/load-specific 호출 완료 \n\n");
        System.out.println("response = " + response);
        return ResponseEntity.ok(ApiResponseEntity.ok(SuccessCode.SUCCESS, response, "해당 과목의 과일바구니 목록"));
    }

    @PostMapping("/add-problem")
    @Operation(summary = "과일바구니에 문제 추가하기", description = "문제를 풀고 특정 과일바구니에 문제 추가할 때 사용하는 API")
    @ApiResponse(responseCode = "200", description = "과일바구니 문제 추가 성공", content = @Content(schema = @Schema(implementation = SuccessCode.class)))
    public ResponseEntity<ApiResponseEntity<Void>> addProblem(@AuthenticationPrincipal CustomUserDetails userDetails,
                                                              @RequestBody ProblemAddRequest request) {
        System.out.println("\n\n Post /api/v1/fruit-basket/add-problem 호출 \n\n");
        System.out.println("userDetails = " + userDetails + ", request = " + request);
        String memberId = userDetails.getUsername();
        fruitBasketService.addProblem(memberId, request);
        System.out.println("\n\n Post /api/v1/fruit-basket/add-problem 호출완료 \n\n");
        return ResponseEntity.ok(ApiResponseEntity.ok(SuccessCode.SUCCESS));
    }

    @PostMapping("/load-problems")
    @Operation(summary = "과일바구니 속 문제 불러오기 API", description = "특정 과일 바구니 속 문제를 불러오는 API")
    @ApiResponse(responseCode = "200", description = "특정 과일바구니 속 문제 로드 성공", content = @Content(schema = @Schema(implementation = ProblemsLoadResponse.class)))
    public ResponseEntity<ApiResponseEntity<ProblemsLoadResponse>> loadProblems(@AuthenticationPrincipal CustomUserDetails userDetails,
                                                                                @RequestBody ProblemsLoadRequest request) {
        System.out.println("\n\n Post /api/v1/fruit-basket/load-problems 호출 \n\n");
        System.out.println("userDetails = " + userDetails + ", request = " + request);
        String memberId = userDetails.getUsername();
        ProblemsLoadResponse response = fruitBasketService.loadProblems(memberId, request);
        System.out.println("\n\n Post /api/v1/fruit-basket/load-problems 호출완료 \n\n");
        System.out.println("response = " + response);
        return ResponseEntity.ok(ApiResponseEntity.ok(SuccessCode.SUCCESS, response, "해당 과목의 과일바구니 목록"));
    }

}
