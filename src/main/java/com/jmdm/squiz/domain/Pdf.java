package com.jmdm.squiz.domain;

import com.jmdm.squiz.enums.SubjectType;
import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity
public class Pdf {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "member_id")
    private Member member;

    @OneToOne(mappedBy = "pdf")
    private Summary summary;

    private String uploadFileName;
    private String storedFileName;
    private String filePath;
    private int totalPageCount;
    private SubjectType subjectType;
    private String kcDataFilePath;
    private String kcDataFileName;

    @OneToMany(mappedBy = "pdf", cascade = CascadeType.REMOVE, orphanRemoval = true)
    private List<Quiz> quizes = new ArrayList<>();

    @Builder
    public Pdf(Long id, Member member, String uploadFileName, SubjectType subjectType, String filePath, String storedFileName, int totalPageCount, String kcDataFilePath, String kcDataFileName) {
        this.id = id;
        setMember(member);
        this.subjectType = subjectType;
        this.uploadFileName = uploadFileName;
        this.filePath = filePath;
        this.storedFileName = storedFileName;
        this.totalPageCount = totalPageCount;
        this.kcDataFilePath = kcDataFilePath;
        this.kcDataFileName = kcDataFileName;
    }

    private void setMember(Member member) {
        this.member = member;
        member.getPdfs().add(this);
    }

    public void setKcDataFilePath(String kcDataFilePath) {
        this.kcDataFilePath = kcDataFilePath;
    }

    public void setSummary(Summary summary) {
        this.summary = summary;
    }
    public void setFilePath(String filePath) { this.filePath = filePath; }
}
