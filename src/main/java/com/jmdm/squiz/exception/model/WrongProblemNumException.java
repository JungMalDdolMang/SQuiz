package com.jmdm.squiz.exception.model;

import com.jmdm.squiz.exception.ErrorCode;

public class WrongProblemNumException extends CustomException{
    public WrongProblemNumException(ErrorCode errorCode, String message) {
        super(errorCode, message);
    }
}
