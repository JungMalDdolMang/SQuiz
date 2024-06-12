package com.jmdm.squiz.domain;

import com.jmdm.squiz.enums.QuizType;
import com.jmdm.squiz.enums.Rank;
import com.jmdm.squiz.enums.SubjectType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity
public class Quiz {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pdf_id")
    private Pdf pdf;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "member_id")
    private Member member;

    private String quizName;
    private SubjectType subjectType;
    private int startPage;
    private int endPage;
    private QuizType quizType;
    private int problemNum;
    private Rank rank;
    private int correctNum;
    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @OneToMany(mappedBy = "quiz", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Problem> problems = new ArrayList<>();
    //Pdf pdf, Member member,
    @Builder
    public Quiz(Long id, String quizName, Pdf pdf, Member member, SubjectType subjectType, int startPage, int endPage, QuizType quizType, int problemNum, Rank rank) {
        this.id = id;
        setPdf(pdf);
        setMember(member);
        this.quizName = quizName;
        this.subjectType = subjectType;
        this.startPage = startPage;
        this.endPage = endPage;
        this.quizType = quizType;
        this.problemNum = problemNum;
        this.rank = rank;
    }
    private void setPdf(Pdf pdf) {
        this.pdf = pdf;
        pdf.getQuizes().add(this);
    }

    private void setMember(Member member) {
        this.member = member;
        member.getQuizs().add(this);
    }
    public void setCorrectNum(int correctNum) {
        this.correctNum = correctNum;
    }
}
