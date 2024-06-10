package com.jmdm.squiz.repository;

import com.jmdm.squiz.domain.Member;
import com.jmdm.squiz.domain.Pdf;
import com.jmdm.squiz.domain.Quiz;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface QuizRepository extends JpaRepository<Quiz, Long> {
    Quiz findByQuizName(String quizName);
    List<Quiz> findAllByPdf(Pdf pdf);
}
