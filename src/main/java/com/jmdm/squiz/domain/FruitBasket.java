package com.jmdm.squiz.domain;

import com.jmdm.squiz.enums.SubjectType;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity
public class FruitBasket {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fruitBasketName;
    private SubjectType subjectType;
    private int problemNum;

    @ManyToOne
    @JoinColumn(name = "member_id")
    private Member member;

    @OneToMany(mappedBy = "fruitBasket", cascade = CascadeType.REMOVE)
    private List<FruitBasketProblem> fruitBasketProblems = new ArrayList<>();

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(updatable = true)
    private LocalDateTime updatedAt;

    @Builder
    public FruitBasket(Long id, String fruitBasketName, SubjectType subjectType, int problemNum, Member member, List<FruitBasketProblem> fruitBasketProblems, LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.id = id;
        this.fruitBasketName = fruitBasketName;
        this.subjectType = subjectType;
        this.problemNum = problemNum;
        setMember(member);
        this.fruitBasketProblems = fruitBasketProblems;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }
    private void setMember(Member member) {
        this.member = member;
        member.getFruitBaskets().add(this);
    }

    public void setProblemNum(int num) {
        this.problemNum = num;
    }
}
