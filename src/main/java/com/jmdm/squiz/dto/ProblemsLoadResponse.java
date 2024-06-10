package com.jmdm.squiz.dto;

import lombok.Data;

import java.util.ArrayList;

@Data
public class ProblemsLoadResponse {
    private String fruitBasketName;
    private ArrayList<ProblemAnswerDTO> problemList;
}
