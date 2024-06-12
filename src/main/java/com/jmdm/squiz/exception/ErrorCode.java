package com.jmdm.squiz.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    CERTIFICATION_NUM_ERROR(HttpStatus.BAD_REQUEST, "인증번호가 일치하지 않습니다."),
    ID_ERROR(HttpStatus.BAD_REQUEST, "이미 존재하는 아이디입니다."),
    EMAIL_NOT_FOUND(HttpStatus.NOT_FOUND, "이메일이 존재하지 않습니다."),
    AI_SERVER_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "ai 서버에서 에러가 발생했습니다."),
    PDF_NOT_FOUND(HttpStatus.NOT_FOUND, "pdf가 존재하지 않습니다."),
    QUIZ_NOT_FOUND(HttpStatus.NOT_FOUND, "quiz가 존재하지 않습니다."),
    FRUIT_BASKET_NOT_FOUND(HttpStatus.NOT_FOUND, "fruit basket이 존재하지 않습니다."),
    PROBLEM_NOT_FOUND(HttpStatus.NOT_FOUND, "problem이 존재하지 않습니다."),
    PROBLEM_GENERATE_FAIL(HttpStatus.INTERNAL_SERVER_ERROR, "문제 생성을 실패했습니다.")
    ;

    private final HttpStatus code;
    private final String message;

    public int getHttpStatusCode() {return code.value();}


}