package com.jmdm.squiz.service;

import com.jmdm.squiz.domain.Member;
import com.jmdm.squiz.dto.MemberDTO;
import com.jmdm.squiz.exception.ErrorCode;
import com.jmdm.squiz.exception.model.DuplicateIdException;
import com.jmdm.squiz.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class MemberService {
    private final MemberRepository memberRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;

    public void checkDuplication(String memberId) {
        if (isDuplicate(memberId)) {
            throw new DuplicateIdException(ErrorCode.ID_ERROR, ErrorCode.ID_ERROR.getMessage());
        }
    }

    private boolean isDuplicate(String memberId) {
        return memberRepository.existsByMemberId(memberId);
    }

    public Member joinMember(MemberDTO request) {
        Member response = Member.toMember(request, bCryptPasswordEncoder);
        memberRepository.save(response);
        return response;
    }


//    public MemberDTO login(MemberDTO memberDTO) {
//        /*
//            1. 회원이 입력한 이메일로 DB에서 조회를 함
//            2. DB에서 조회한 비밀번호와 사용자가 입력한 비밀번호가 일치하는지 판단
//         */
//        Optional<Member> byMemberEmail = memberRepository.findByMemberEmail(memberDTO.getMemberEmail());
//        if (byMemberEmail.isPresent()) {
//            // 조회 결과가 있다(해당 이메일을 가진 회원정보가 있다)
//            Member member = byMemberEmail.get();
//            if (member.getMemberPassword().equals(memberDTO.getMemberPassword())) {
//                // 비밀번호가 일치하는 경우
//                // entity -> dto 변환 후 리턴
//                MemberDTO dto = MemberDTO.toMemberDTO(member);
//                return dto;
//            } else {
//                // 비밀번호 불일치(로그인 실패)
//                return null;
//            }
//        } else {
//            // 조회 결과가 없다(해당 이메일을 가진 회원이 없다)
//            return null;
//        }
//    }
}
