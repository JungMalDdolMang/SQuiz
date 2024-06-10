package com.jmdm.squiz.controller;

import com.jmdm.squiz.dto.EmailCertificationRequest;
import com.jmdm.squiz.dto.EmailCertificationResponse;
import com.jmdm.squiz.dto.PdfUploadResponse;
import com.jmdm.squiz.exception.SuccessCode;
import com.jmdm.squiz.service.MailSendService;
import com.jmdm.squiz.service.MailVerifyService;
import com.jmdm.squiz.utils.ApiResponseEntity;
import io.swagger.v3.oas.annotations.Operation;

import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;

import jakarta.mail.MessagingException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.security.NoSuchAlgorithmException;

@RestController //@Controller + @ResponseBody
@RequiredArgsConstructor
@RequestMapping("/api/v1/email")
@Tag(name = "이메일 인증 API", description = "이메일 인증 코드를 전송하고, 인증코드를 검증하는 API입니다.")
public class MailController {
    private final MailSendService mailSendService;
    private final MailVerifyService mailVerifyService;

    @PostMapping("/send-certification")
    @Operation(summary = "인증 코드를 전송", description = "사용자의 이메일로 인증코드를 전송하는 API")
    @ApiResponse(responseCode = "200", description = "이메일 인증 성공", content = @Content(schema = @Schema(implementation = EmailCertificationResponse.class)))
    public ResponseEntity<ApiResponseEntity<EmailCertificationResponse>> sendCertificationNumber(@Validated @RequestBody EmailCertificationRequest request)
            throws MessagingException, NoSuchAlgorithmException {
        System.out.println("\n\n Post /api/v1/email/send-certification 호출 \n\n");
        System.out.println("request = " + request);
        EmailCertificationResponse response = mailSendService.sendEmailForCertification(request.getEmail());
        System.out.println("\n\n Post /api/v1/email/send-certification 호출 완료 \n\n");
        System.out.println("response = " + response);
        return ResponseEntity.ok(ApiResponseEntity.ok(SuccessCode.EMAIL_SEND_SUCCESS, response, "인증할 메일과 인증 코드"));
    }

    @PostMapping("/verify")
    @Operation(summary = "인증코드 확인", description = "인증코드가 올바른지 확인하는 API")
    @ApiResponse(responseCode = "200", description = "인증코드 일치")
    public ResponseEntity<ApiResponseEntity<Void>> verifyCertificationNumber(@RequestBody EmailCertificationResponse request) {
        System.out.println("\n\n Post /api/v1/email/verify 호출 \n\n");
        System.out.println("request = " + request);
        mailVerifyService.verifyEmail(request.getEmail(), request.getCertificationNumber());
        System.out.println("\n\n Post /api/v1/email/verify 호출 완료 \n\n");
        System.out.println("request = " + request);
        return ResponseEntity.ok(ApiResponseEntity.ok(SuccessCode.SUCCESS));
    }
}
