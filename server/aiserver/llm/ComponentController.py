class ComponentController:

    def choice_quiz_create_msg(self, params):
        """
        GPT API 호출할 때 필요한 message (프롬프트) 생성

        :param params: { pdftxt: str, rank: str, problem_num: str, subject: str }
        :return: message
        """

        subject = params["subject"]
        problem_num = params["problem_num"]
        if params["rank"] == "LOWER":
            rank = "EASY."
        elif params["rank"] == "MIDDLE":
            rank = "MIDDLE."
        elif params["rank"] == "UPPER":
            rank = "ADVANCED."
        else:
            rank = "MIDDLE"

        print(f"과목: {subject}")
        print(f"문제 난이도: {rank}")
        example_choice = ""

        if subject == "OPERATING_SYSTEM":
            example_choice =  "[example1] question: A process’ virtual address space contains the segments for code, heap, stack, data and BSS. When the program is loaded onto memory for execution, OS initializes the some of the segments with the contents loaded from the disk. Consider the following code. Among the five segments listed above, which segment is initialized with respect to the contents from the binary file? int a_array [1000] ; int b_array [1000] = 0 ; main(){ int first_integer ; static int second_integer ; //;;; } options: a: a_array, b: b_array, c: first_integer, d: second_integer answer: b" \
                              "[example2] question: A currently running process has used up its time quantum. Then, the CPU scheduler schedules the next process from the queue of processes that are waiting to be executed. What is the state of process that has been running after it has used up its time quantum? options: a: RUNNING, b: READY, c: BLOCKED, d: SUSPENDED"\
                              "[example3] question: A system that can only execute one program at a time is? options: a: hard wiring system, b: batch job system, 3: time sharing system, 4: real-time system answer: b"\
                              "[example4] Question: Compared to non-preemptive scheduling, which statement about preemptive scheduling is incorrect? Options: a: It has a lower priority compared to non-preemptive scheduling. b: It can interrupt a running task and execute a new task. c: It has a lot of context switch overhead. d: It is used in time-sharing schedulers. Answer: b"\
                              "[example5] Question: Which explanation about the four necessary conditions for deadlock is incorrect? Options: a: Mutual Exclusion: Deadlock occurs when the resources used by one process are exclusive and cannot be shared with other processes. b: Non-preemption: Deadlock occurs when a resource being used by one process is preempted by another process in the middle of its usage. c: Hold and Wait: Deadlock occurs when a process holds some resources and waits for other resources. d: Circular Wait: Deadlock occurs when the relationship of processes holding resources and waiting for others forms a circle, and none of the processes can proceed. Answer: b"

        elif subject == "C_LANGUAGE":
            example_choice = "[Example1] KC: 운영체제의 메모리 관리 방법, Question: 운영체제에 따라 포인터 변수의 크기는 고정됩니다. 32비트 운영체제에서 포인터 변수의 크는 얼마인가?, A: 2byte, B:4byte, C:8byte, D:16byte, Answer: B " \
                             "[Example2] KC: 2진수를 16진수로 변환하는 방법, Question: 2진수 0000 0000 1000 1110을 16진수로 나타내면 무엇인가?, A: 0x008E, B: 0x00E7, C: 0x007D, D: 0x008D, Anser: A " \
                             "[Example3] KC: 비트 연산자, Question: 0000 1111과 0011 1100을 XOR 계산한 결과는 무엇인가?, A: 0011 0011, B: 0011 1100, C: 1100 1100, D: 1100 0000, Answer: A " \
                             "[Example4] KC: extern 키워드, Question: 같은 프로젝트 안에 존재하는 전역 변수를 참조하겠다는 의미를 가진 키워드는 무엇인가?, A: static, B: extern, C:const, D: private, Answer: B " \
                             "[Example5] KC:배열 시작 주소, Question: char data[4]; char p = &*data[0];일때 의미가 다른 표현은 무엇인가?, A: data, B: &*(data+0), C:&data, D:&(*data), Answer:C"

        elif subject == "COMPUTER_COMMUNICATION":
            example_choice = "[Example1] KC: ICMP: The Internet Control Message Protocol Question: ICMP 프로토콜에 대한 설명으로 올바른 것을 고르시오. A: TCP/IP 기반의 통신망에서 전송 과정에 문제가 발생하면 수신 호스트에 의해 ICMP 메시지가 자동으로 발생한다.B: ICMP에 의해 발생하는 메시지의 종류는 오류 보고 메시지와 질의 메시지로 나뉜다.C: 오류 보고 메시지는 IP 패킷을 전송하는 과정에서 발생하는 문제를 보고하는 것이 목적이며, 수신 호스트에 전달된다.D: ICMP는 단순히 오류 발생 사실을 통보하는 것이므로 오류를 해결하는 것은 하위 계층의 몫이다. Answer: 2 " \
                             "[Example2] KC: IPv6 Question:  IPv6 프로토콜의 장점에 대한 설명으로 ****올바른 것을 고르시오. A: 호스트의 주소 공간을 대폭 축소한 IPv6은 기존 인터넷 환경에서 사용하는 IPv4를 대체하기 위한 차세대 프로토콜이다. B: 송신 호스트와 수신 호스트의 주소를 표시하는 공간이 32비트에서 64비트로 확장되었다. C: IPv6 헤더는 불필요한 필드가 제외되거나 확장 헤더 형식으로 변경되었다. D: 흐름 제어 기능을 지원할 수 있는 필드를 도입해 일정 범위 내에서 예측 가능한 데이터 흐름을 지원한다. Answer: C " \
                             "[Example3]Question: 라우팅 알고리즘에 대한 설명으로 잘못된 것을 고르시오. A: 네트워크에서 거리의 기준은 다양하지만, 라우팅과 관련해 가장 보편적으로 이용하는 기준은 전송 경로의 중간에 위치하는 라우터의 개수인 홉 수로 판단하는 것이다. B:  최단 경로 라우팅 방식은 패킷이 목적지에 도달할 때까지 거치는 라우터 수가 최소화되도록 경로를 선택한다. C: 홉 수 외에 거리 기준이 될 수 있는 요소에는 패킷의 전송 지연 시간, 전송 대역폭, 통신 비용 등이 있다. D: 플러딩은 라우터가 자신에게 입력된 패킷의 출력을 최소화하는 방식이다. Answer: D " \
                             "[Example4]KC: The 802.11 MAC Protocol Question: MAC 계층에 대한 설명으로 올바른 것을 고르시오. A: LAN 환경에서는 WAN 환경보다 효율적인 전송 관리를 통해 네트워크의 전송 효율을 극대화해야 한다. B: 토큰 링 방식은 공유 버스의 순환 구조를 지원하며, 토큰이라는 특정 패턴의 제어 프레임이 링을 순환한다. C: MAC 계층은 전송 선로의 물리적인 특성을 반영하므로 WAN의 종류에 따라 특성이 구분된다. D: 토큰 버스는 공유 버스를 이용해 호스트를 연결하는 CSMA/CD 방식을 지원한다. Answer: A " \
                             "[Example5]Question: OSI 7계층 모델에 대한 설명으로 잘못된 것을 고르시오. A: 다수의 시스템을 서로 연결해서 통신하려면 선행적으로 연결 방식을 표준화해야 한다. B: 데이터 전송 과정에서 송수신 호스트 사이의 라우터들이 중개 기능을 수행한다. 일반적으로 라우터는 하위 3개 계층의 기능만 수행한다. C: OSI 7계층 모델에 따르면, 네트워크에 연결된 호스트들은 7개 계층으로 모듈화된 전송 기능을 갖추어야 한다. D: 일반 사용자는 OSI 7계층 맨 아래에 있는 물리 계층을 통해 데이터의 송수신을 요청한다. Answer: D "

        elif subject == "OBJECT_ORIENTED_PROGRAMMING":
            example_choice = "[Example1] KC:자바프로그램 구성 요소 Question:다음 중에서 올바른 주석이 아닌 것을 고르시오. A:/** 주석 */ B:/* 주석 */ C:/* 주석 D:// 주석 Answer:C " \
                             "[Example2] KC:배치 관리자 Question:컨테이너의 영역을 동서남북, 중앙의 5개 영역으로 구분하여 컴포넌트를 배치하는 배치관리자는 무엇인가? A:FlowLayout B:BorderLayout C:GridLayout D:CardLayout Answer:B " \
                             "[Example3] KC:이벤트 처리 방법 Question:버튼을 누르면 발생하는 이벤트는 무엇인가? A:ActionEvent B:MouseEvent C:ItemEvent D:KeyEvent Answer:A " \
                             "[Example4] KC:이벤트 처리 개요 Question:다음 중 액션 이벤트를 발생시키지 않는 위젯은 무엇인가? A:버튼 B:메뉴 항목 C:텍스트 필드 D:스크롤바 Answer:D " \
                             "[Example5] KC:배치 관리자 Question:컨테이너 p의 배치관리자를 제거하려면 어떻게 하여야 하는가? A:p.setLayout(); B:p.setLayout(0); C:p.setLayout(null); D:p.setLayout(false); Answer:C"

        sys_content_for_choice = (
                "You will receive the knowledge component (KC) and the contents of the corresponding learning materials."
                "KC is a unit of learning concept. For example, in operating system subjects, process concepts, "
                "system calls, etc. can be KC."
                "You will create " + problem_num + "multiple-choice quiz for a student studying operating systems. "
                "Create a question and four options: a, b, c, and d."
                "Don't create duplicate questions, and there should be no multiple correct answers. The correct answer must be unambiguously clear to anyone without any room for controversy."
                "Select one KC among the given KCs and create a problem to check the concept."
                "Problems must be created based on the content of the study material corresponding to the selected KC."
                "kc and corresponding learning materials will be entered in the form of <kc ID>kc: learning material "
                "content, such as <0> Operating system definition: Operating system is ...., <14> Process concept: "
                "Process is, ... ."
                "Base the questions on the given learning materials, but ensure the questions are fact-based, as the learning materials may contain noise."
                "Create a problem and call the get_problem function. "
                "Please make the problem difficulty level " + rank +
                "Select one KC and KC ID in the given material and create a problem to check the concept, KC."
                "Each KC (Knowledge Component) must have a unique ID value. Always select the KC and its corresponding KC ID as a pair. They should not be changed."
                "You must create " + problem_num + "problems."
                "Keep in mind that you must create problems according to the given number of problems. "
        )

        dkt = params['dkt']

        if dkt and len(dkt) >= 2:
            sorted_dkt = sorted(dkt, key=lambda x: x["predict"])
            kc_list = [sorted_dkt[0]["kcId"], sorted_dkt[1]["kcId"]]            

            sys_content_for_choice += "Keep in mind that more than half of the total problems must be created for the following KC IDs: " + ", ".join(map(str, kc_list)) + ". Keep in mind that These KC IDs are of utmost importance and require a higher number of problems than other KC IDs."


        user_content_for_choice = (
                "Create " + problem_num + "multiple-choice, four-choice problems for learning operating systems. "
                "If you give me a learning concept and corresponding learning materials, select a learning concept from "
                "among them and create a problem based on the data."
                "Choose one kc for each problem. And make all the problems in Korean."
                "You have to make " + problem_num + "problems. "
                "Please make the problem difficulty level " + rank +
                "Keep in mind that you must create problems according to the given number of problems."
                "[knowledge component and study material]: " + params["pdftxt"] +
                "Create " + problem_num + "multiple-choice problems."
        )

        msg_for_choice = [
            {"role": "system", "content": sys_content_for_choice + example_choice},
            {"role": "user", "content": user_content_for_choice}
        ]

        return msg_for_choice

    def ox_quiz_create_msg(self, params):
        """
        GPT API 호출할 때 필요한 message (프롬프트) 생성

        :param params: { pdftxt: str, rank: str, problem_num: str, subject: str }
        :return: message
        """

        subject = params["subject"]
        problem_num = params["problem_num"]
        if params["rank"] == "LOWER":
            rank = "EASY."
        elif params["rank"] == "MIDDLE":
            rank = "MIDDLE."
        elif params["rank"] == "UPPER":
            rank = "ADVANCED."
        else:
            rank = "MIDDLE"

        print(f"과목: {subject}")
        print(f"문제 난이도: {rank}")

        example_ox = ""

        if subject == "OPERATING_SYSTEM":
            example_ox = "[example1] question: 배열을 원소를 초기화하지 않고 선언만 해도 컴파일 시점에 초기화된다. answer: false" \
                         "[example2] question: A process has requested an IO to read a disk page from the storage device. The process is waiting for the completion of an IO. The disk has transferred the requested page from the disk to the host’s memory. After the IO request completes, the state of process that has been waiting for the IO completion is BLOCK." \
                         "[example3] question: batch job system은 한 번에 여러 프로그램을 실행할 수 있다. answer: false" \
                         "[example4] question: You can mitigate starvation through aging. answer: true. " \
                         "[example5] question: 스냅숏은 데이터베이스나 운영체제 시스템에서 에러가 발생하여 특정 지점으로 돌아가는 행위를 가리킨다. answer: false."

        elif subject == "C_LANGUAGE":
            example_ox = "[Example1] KC: 포인터 변수의 주소 연산, Question: int *형으로 선언한 포인터 p 변수에 200번지가 저장되어있다. p++; 명령을 수행하고 나면 p에 저장된 주소는 201번지이다. Answer:X " \
                         "[Example2] KC: 동적 메모리 할당 및 해제, Question: p에 할당된 메모리를 해제할 때는 free(p)를 하면 된다. Answer: O " \
                         "[Example3] KC: 2진수를 16진수로 변환하는 방법, Question: 16진수 0x1C6A는 2진수 0001 1100 0110 1010으로 나타낼 수 있다., Answer: O " \
                         "[Example4] KC: 컴퓨터의 자료 기억 방식, Question: 운영체제는 메모리에 비트 단위로 주소를 부여해 관리한다., Answer: X " \
                         "[Example5] KC: 전처리기, Qustion: 프로그래머가 원하는 사항을 컴파일러에 직접 지시하는 문법을 기계어라고 한다., Answer: X"

        elif subject == "COMPUTER_COMMUNICATION":
            example_ox = "[Eaample1]KC: ICMP: The Internet Control Message Protocol Question: ICMP는 단순히 오류 발생 사실을 통보하는 것이므로 오류를 해결하는 것은 하위 계층의 몫이다. Answer: X " \
                         "[Eaample2]KC: IPv6 Question:  호스트의 주소 공간을 대폭 축소한 IPv6은 기존 인터넷 환경에서 사용하는 IPv4를 대체하기 위한 차세대 프로토콜이다. Answer: X " \
                         "[Eaample3]Question:  최단 경로 라우팅 방식은 패킷이 목적지에 도달할 때까지 거치는 라우터 수가 최소화되도록 경로를 선택한다. Answer: O " \
                         "[Eaample4]KC: The 802.11 MAC Protocol Question: LAN 환경에서는 WAN 환경보다 효율적인 전송 관리를 통해 네트워크의 전송 효율을 극대화해야 한다. Answer: O " \
                         "[Eaample5]Question: OSI 7계층 모델에 따르면, 네트워크에 연결된 호스트들은 7개 계층으로 모듈화된 전송 기능을 갖추어야 한다. Answer: O"

        elif subject == "OBJECT_ORIENTED_PROGRAMMING":
            example_ox = "[Example1] KC: 클래스와 객체 만들기 Question: 하나의 자바 파일에 2개의 public 클래스를 넣을 수 있는가? Answer:X " \
                         "[Example2] KC: 생성자와 메소드 오버로딩 Question:생성자에서 다른 메소드를 호출할 수 있는가? Answer:O " \
                         "[Example3] KC: 생성자와 메소드 오버로딩 Question: 생성자를 사용하지 않고 인스턴스 변수들을 초기화할 수 있는가? Answer: O " \
                         "[Example4] KC: 자바 GUI 소개 Question: 운영체제에 따라서 GUI 컴포넌트의 모양이 달라지는 것은 스윙이 아닌 AWT이다. Answer: O " \
                         "[Example5] KC: 컨테이너 살펴보기 Question:패널은 최상위 컨테이너인가? Answer:X"

        sys_content_for_ox = (
                "You will receive the knowledge component (KC) and the contents of the corresponding learning materials."
                "KC is a unit of learning concept. For example, in operating system subjects, process concepts, "
                "system calls, etc. can be KC."
                "Create true/false questions for studying operating systems. Answers should be either 'true' or 'false'. "
                "Don't create duplicate questions, and there should be no multiple correct answers. The correct answer must be unambiguously clear to anyone without any room for controversy."
                "Please make the problem difficulty level " + rank +
                "Select one KC among the given KCs and create a problem to check the concept."
                "Problems must be created based on the content of the study material corresponding to the selected KC."
                "kc and corresponding learning materials will be entered in the form of <kc ID>kc: learning material "
                "content, such as <0> Operating system definition: Operating system is ...., <14> Process concept: "
                "Process is, ... ."
                "Base the questions on the given learning materials, but ensure the questions are fact-based, as the learning materials may contain noise."
                "Create a problem and call the get_problem function."
                "Select one KC and KC ID in the given material and create a problem to check the concept, KC."
                "Each KC (Knowledge Component) must have a unique ID value. Always select the KC and its corresponding KC ID as a pair. They should not be changed."
                "You must create " + problem_num + "problems."
                "Keep in mind that you must create " + problem_num + "problems."
        )

        dkt = params['dkt']

        if dkt and len(dkt) >= 2:
            sorted_dkt = sorted(dkt, key=lambda x: x["predict"])
            kc_list = [sorted_dkt[0]["kcId"], sorted_dkt[1]["kcId"]]            
            
            sys_content_for_ox += "Keep in mind that more than half of the total problems must be created for the following KC IDs: " + ", ".join(map(str, kc_list)) + ". Keep in mind that These KC IDs are of utmost importance and require a higher number of problems than other KC IDs."

        user_content_for_ox = (
                "Create " + problem_num + "true/false problems for learning operating systems. "
                "If I give you a learning concept and corresponding learning materials, select a learning concept from "
                "among them and create a problem based on the data."
                "Choose one kc for each problem. And make all the problems in Korean."
                "You have to make " + problem_num + "problems. "
                "Please make the problem difficulty level " + rank +
                "Keep in mind that you must create problems according to the given number of problems."
                "[knowledge component and study material]: " +
                params["pdftxt"] +
                "Create " + problem_num + "true/false problems."
        )

        msg_for_ox = [
            {"role": "system", "content": sys_content_for_ox + example_ox},
            {"role": "user", "content": user_content_for_ox}
        ]

        return msg_for_ox

    def blank_quiz_create_msg(self, params):
        """
        GPT API 호출할 때 필요한 message (프롬프트) 생성

        :param params: { pdftxt: str, rank: str, problem_num: str, subject: str }
        :return: message
        """

        subject = params["subject"]
        problem_num = params["problem_num"]
        if params["rank"] == "LOWER":
            rank = "EASY."
        elif params["rank"] == "MIDDLE":
            rank = "MIDDLE."
        elif params["rank"] == "UPPER":
            rank = "ADVANCED."
        else:
            rank = "MIDDLE"
        print(f"과목: {subject}")
        print(f"문제 난이도: {rank}")

        example_blank = ""

        if subject == "OPERATING_SYSTEM":
            example_blank = (
                "[example1]  question: A process’ virtual address space contains the segments for code, heap, stack, ""data and BSS.""When the program is loaded onto memory for execution, OS initializes the some of the segments with ""the contents loaded from the disk.""Consider the following code. ""There are four variable declarations in the code above. They are numbered from (1) to (4). ""Specify the segment where each of these variables resides.""content:int a_array [1000] ; //—(1) int b_array [1000] = 0 ; // —(2) main(){ int first_integer ; // ""—(3) static int second_integer ;// —(4)//; }"
                "[example2] question: A process can have one of the three states: RUNNING, READY and BLOCKED. Please ""fill in the blank to the following.""content: What is the state of the process that is currently being executed by CPU?""The state of the process that is currently being executed by CPU is ___ (1) ___.""A process that has been running is now waiting for the user input. ""The state of process when the process is waiting for the user input is ___ (2) ___.""You must create 10 problems. "
                "[example3] question: Fill in the blanks.""content: A system that can only execute one program at a time is ___ (1) ___.""A system that divides CPU time finely to make it appear that multiple programs are running ""simultaneously is ___ (2) ___.""blanks: blank_1: batch job system, blank_2: time sharing system"
                "[example4] question: Fill in the blank.""content: ___ (1) ___ is a kernel that provides only the most basic functions such as process ""management, memory management, and inter-process communication management.""blank_1: microkernel"
                "[example5] question: The following are descriptions of scheduling algorithms. Fill in the blanks ""with appropriate answers.""content: The non-preemptive scheduling algorithm that assigns the CPU in the order in which ""processes arrive in the ready queue is ___ (1) ___.""The non-preemptive scheduling algorithm that assigns the CPU to the job with the shortest execution ""time among the processes in the ready queue is ___ (2) ___.""blanks: blank_1: Highest Response Ratio Next (HRRN), blank_2: Shortest Job First (SJF)"
            )

        elif subject == "C_LANGUAGE":
            example_blank = "[Example1] KC: if 조건문, Question: result 변수의 값이 음수이면 양수로 변경하는 예제를 만들고자 한다. 빈칸에 들어갈 코드를 작성하시오.(단 result 변수가 0인 경우는 포함하지 않는다.), Content: int result = -5; if(__(1)__) result= rsult * (-1);, Answer: result < 0 " \
                            "[Example2] KC: 포인터, Question: 빈칸에 들어갈 코드를 작성하시오., Content: #include <stdio.h> void main() { short birthday; short __(1)__ ptr; ptr __(2)__ birthday; __(3)__ ptr = 0X0412; printf(\"birthday = &d (0x%04X)\n\", birthday, birthday) },  Blank1:*, Blank2:&, Blank3:* " \
                            "[Example3] KC:  동적 메모리 할당 및 해제, Question: 200byte 메모리를 동적으로 할당할 때 4byte씩 50개 그룹으로 사용하려고 한다. 빈칸에 들어갈 코드를 작성하시오., Content: int *p = (__(1)__))malloc(__(2)__)),  Blank1: int, Blank2: 200 " \
                            "[Example4] KC: 변수, Question: 빈칸에 알맞은 말을 채우시오, Content: __(1)__는 데이터를 저장하기 위한 메모리 공간을 의미 합니다., Blank1: 변수 " \
                            "[Example5] KC: 아스키코드, Question: 빈칸에 알맞은 말을 채우시오., Content: 컴퓨터에서 문자를 숫자로 바꾸어 저장하는 표준 형식을  __(1)__라고 합니다., Blank1: 아스키코드"

        elif subject == "COMPUTER_COMMUNICATION":
            example_blank = "[Example1]KC: ICMP: The Internet Control Message Protocol Question: 다음은 ICMP 프로토콜에 대한 설명이다. 빈칸에 알맞은 것을 적으시오. Content: ICMP에 의해 발생하는 메시지의 종류는 오류 보고 메시지와 ___ (1) ___ 메시지로 나뉜다. Blank1: 질의 " \
                            "[Example2]KC: IPv6 Question:  IPv6 프로토콜의 장점에 대한 설명이다. 빈칸을 채우시오. Content: 호스트의 ___ (1) ___을 대폭 확장한 IPv6은 기존 인터넷 환경에서 사용하는 ___ (2) ___를 대체하기 위한 차세대 프로토콜이다. Blank1: 주소 공간 Blank2: IPv4 " \
                            "[Example3]Question: 라우팅 알고리즘에 대한 설명이다. 빈칸을 채우시오. Content:  최단 경로 라우팅 방식은 패킷이 목적지에 도달할 때까지 거치는 ___ (1) ___ 수가 최소화되도록 경로를 선택한다. Blank1: 라우터 " \
                            "[Example4]Question: MAC 계층에 대한 설명으로 올바른 것을 고르시오. Content: ___ (1) ___ 환경에서는 WAN 환경보다 효율적인 전송 관리를 통해 네트워크의 전송 효율을 극대화해야 한다. Blank1: LAN " \
                            "[Example5]Question: OSI 7계층 모델에 대한 설명으로 잘못된 것을 고르시오. Content: 다수의 시스템을 서로 연결해서 통신하려면 선행적으로 연결 방식을 ___ (1) ___해야 한다. OSI 7계층 모델에 따르면, 네트워크에 연결된 호스트들은 7개 계층으로 ___ (2) ___된 전송 기능을 갖추어야 한다. Blank1: 표준화 Blank2: 모듈화"

        elif subject == "OBJECT_ORIENTED_PROGRAMMING":
            example_blank = "[Example1] KC:배열 Question:빈칸에 들어갈 코드를 작성하시오 Content: public class ArrayTest{ public static void main(String[] args){ int[] numbers = {10, 20, 30}; for (___(1)___) ___(2)___ ; } } // output: 10 20 30 Blank1:int value: numbers Blank2:System.out.print(value+" "); "\
                            "[Example2] KC: 컨테이너 살펴보기 Question:빈칸에 알맞은 말을 채우시오. Content:프레임에서 컴포넌트를 붙일 수 있는 영역을 ___(1)___라고 한다. Blank1:Content Pane "\
                            "[Example3] KC:이벤트 처리 개요 Question:빈칸에 알맞은 말을 채우시오. Content:발생된 이벤트 객체에 반응하여 이벤트를 처리하는 객체를 ___(1)___ 라고 한다. Blank1:이벤트 리스너 "\
                            "[Example4] KC: 배치 관리자 Question:패널 p에 4 X 3 격자 모양으로 위젯들을 배치하려 한다. 배치관리자를 설정하는 아래의 코드의 빈칸에 들어갈 코드를 작성하시오. Content: p.setLayout( ___(1)___ ); Blank1:new GridLayout(4, 3) "\
                            "[Example5] KC:기본 도형 그리기 Question:(0,0)을 왼쪽 상단으로 하고 크기가 100 X 100인 사각형을 그리고자 한다. 빈칸에 들어갈 코드를 작성하시오. Content:class MyPanel extends JPanel{ public void paintComponent(Graphics g){ super.paintComponent(g); ___(1)___ ; } } Blank1:g.drawRect(0, 0, 100, 100);"

        if subject != "C_LANGUAGE":
            sys_content_for_blank = (
                "You will receive the knowledge component (KC) and the contents of the corresponding learning materials."
                "KC is a unit of learning concept. For example, in operating system subjects, process concepts, system calls, etc. can be KC. "
                "Create fill-in-the-blank questions for studying operating systems. "
                "The number of blanks should be minimum one and maximum four."
                "Create content consisting of learning concepts or programming code, and create blanks in the content. "
                "Don't create duplicate questions, and there should be no multiple correct answers. The correct answer must be unambiguously clear to anyone without any room for controversy."
                "For subjects like C language or object-oriented programming, appropriately generate code problems to assess code comprehension."
                "If it is a code problem, provide a string in Markdown format that can be rendered as a code block."
                "If a code problem is generated, write the content in Markdown format and check is_markdown as true."
                "And remember to indicate the code block language at the beginning, such as ```c or ```java, to ensure it is rendered as a code block."
                "Blanks should be in the format of ___ (1) ___, ___ (2) ___, including IDs, starting from the first blank. "
                "Keep in mind to create the blanks sequentially starting from number 1. "
                "Place three underscores before and after the blanks. "
                "Select one KC and KC ID in the given material and create a problem to check the concept, KC."
                "Problems must be created based on the content of the study material corresponding to the selected KC."
                "Each KC (Knowledge Component) must have a unique ID value. Always select the KC and its corresponding KC ID as a pair. They should not be changed."
                "kc and corresponding learning materials will be entered in the form of <kc ID>kc: learning material content, such as <0> Operating system definition: Operating system is ...., <14> Process concept: Process is, ... ."
                "Create a problem and call the get_problem function."
                "Base the questions on the given learning materials, but ensure the questions are fact-based, as the learning materials may contain noise."
                "Don't forget to indicate code blocks with something like ```c to create code blocks."
                "You must create " + problem_num + " problems. "
                "Please make the problem difficulty level " + rank +
                "Keep in mind that you must create problems according to the given number of problems.")
   
        else:
            sys_content_for_blank = (
            # '너는 각 knowledge component(KC) 별로 구분된 수엽용 학습자료를 받을거야. 그리고 각 KC와 학습자료를 기반으로 빈칸 문제를 만들어야해.'
            # "주어진 개수만큼 주어진 난이도에 맞춰 문제를 생성해"
            # "KC는 학습에 단위가 되는 거야. 각 KC는 그들을 식별하는 KC ID를 가지고 있어."
            # "학습자료는 다음과 같은 형태로 입력될 거야. <KC ID> KC: 학습 내용. KC ID와 KC는 임의로 정해진 쌍이기 때문에 항상 둘이 대응되어야 해."
            # "너는 주어진 입력 중에 KC를 택하고 해당 학습 자료에 기반하여 해당 개념을 확인할 수 있는 빈칸 문제를 만들어."
            # "빈칸 문제는 답이 명확해야해. 단답식으로 답을 낼 수 있도록 짧고 명확하게 만들어야 해."
            # "한 문제당 빈칸의 개수는 최소 1개에서 최대 4개까지 있을 수 있어."
            # "빈칸은 1번부터 시작해야해 하고, ___ (1) ___, ___ (2) ___ 이런식으로 빈칸을 표시하도록 해."
            # "빈칸이 포함되는 content와 해당 content에 대한 설명과 content에 대한 짧은 설명과 '빈칸을 채우시오'와 같은 지시문을 포함하는 Question을 만들어"
            # "코드 빈칸 채우기 같은 코드 관련 문제도 낼 수 있어. 코드 관련 문제의 경우에는 content는 보기좋게 렌더링하기 위해 마크다운 포맷의 문자열로 출력해야해."
            # "코드의 경우 코드 블럭으로 만들기 위해 ```c 와 같이 코드블럭을 나타내는 문자열이 포함되어야 해."
            # "문제를 생성해서 get_pronlem 함수를 호출해"
            # "그리고 가장 중요한 건 문제는 주어진 개수 만큼 만들어야 한다는 것을 명심해."
            # "KC는 임의로 생성하지 말고, 주어진 자료에 기반해서 선택해."
            # "문제는 짧게 간결하고 명확하게 만들도록 해."
            # "또한 문제 난이도는 ADVANCED 레벨로 만들어야 해."
            "You will receive learning materials segmented by each knowledge component (KC). Based on each KC and the learning materials, you need to create fill-in-the-blank questions."

            f"Generate the {problem_num}questions matching the given difficulty level {rank}."

            "KC is a unit used for learning. Each KC has a KC ID that identifies them."

            "The learning materials will be provided in the following format: <KC ID> KC: learning content. Since KC IDs and KCs are arbitrarily paired, they must always correspond to each other."

            "Choose a KC from the given inputs and create fill-in-the-blank questions based on the corresponding learning material to verify that concept."

            "The fill-in-the-blank questions must have clear answers. Make them short and precise so that they can be answered in a single word or phrase."

            "There should be at least 1 and at most 4 blanks per question."

            "Blanks should start from number 1, and be indicated as ___ (1) ___, ___ (2) ___ in the content."

            "Create a question that includes the content with blanks, a short explanation of the content, and an instruction like 'Fill in the blanks'."

            "You can also create code-related questions like code fill-in-the-blank. In the case of code-related questions, the content should be output as a string in markdown format for better rendering."

            "For code, the string should include code blocks indicated by ```c to represent code blocks."

            "Generate the questions and call the get_pronlem function."

            f"Most importantly, remember that you must create the {problem_num} questions."

            "Do not arbitrarily generate KCs; select them based on the given materials."

            "Make the questions short, concise, and clear."
            
            "Ensure that the answers for the blanks are composed of a single word, not a sentence or a verb."
            
            "You should create blanks in places that can be inferred solely from the content."

            f"Also, make the difficulty level of the questions {rank}"
            
            "There may be noise in the learning materials, so create questions based on the learning materials, but ensure they are based solely on facts."

            "Do not create questions that can have multiple correct answers or questions that are too similar to each other."

            )

        dkt = params['dkt']
        print("Hi")
        if dkt and len(dkt) >= 2:
            sorted_dkt = sorted(dkt, key=lambda x: x["predict"])
            kc_list = [sorted_dkt[0]["kcId"], sorted_dkt[1]["kcId"]]            
            
            sys_content_for_blank += "Keep in mind that more than half of the total problems must be created for the following KC IDs: " + ", ".join(map(str, kc_list)) + ". Keep in mind that These KC IDs are of utmost importance and require a higher number of problems than other KC IDs."


        user_content_for_blank = (
                "Create " + problem_num + "fill-in-blank problems for learning operating systems. "
                "If you give me a learning concept and corresponding learning materials, select a learning concept from "
                "among them and create a problem based on the data."
                "Choose one kc for each problem. And make all the problems in Korean."
                "You have to make " + problem_num + "problems. "
                "Please make the problem difficulty level " + rank +
                "Keep in mind that you must create problems according to the given number of problems."
                "[knowledge component and study material]: " + params["pdftxt"] +
                "Create " + problem_num + "fill-in-blank problems."
        )

        msg_for_blank = [
            {"role": "system", "content": sys_content_for_blank + example_blank},
            {"role": "user", "content": user_content_for_blank}
        ]

        return msg_for_blank

    def summary_create_msg(self, params):
        """
        GPT API 호출할 때 필요한 message (프롬프트) 생성

        :param params: { pdftxt: str, subject: str }
        :return: message
        """

        subject = params["subject"]
        example_summary = ""

        if subject == "OPERATING_SYSTEM":
            example_summary = (
                "[example1] # Ch1. Introduction ## Operating system : 컴퓨터의 구성요소들을 관리하는 소프트웨어 레이어 **컴퓨터의 구성** - 소프트웨어: 응용 프로그램과 운영체제 - 하드웨어: 프로세서, 메인메모리, 디스크, 입출력 장치 ### **OS의 역할** : 동시에 여러 프로그램을 실행할 수 있게 하는 역할 - ***자원 관리자*** - memory, I/O devices와 다른 자원들을 보호하고 관리 - time, space에 따른 자원 공유 - 명령어 집합과 그의 자원을 관리 ### 운영체제 역사 | 1945-55 | Vacuum Tubes | | --- | --- | | 1955-65 | Transistors and Batch System | | 1965-80 | ICs and Multiprogramming | | 1980~ | Personal Computer | ## 하드웨어 - **CPU** : memory로 부터 명령어 읽어와서 수행. - **Memory** : 실행 중인 프로그램을 적재. - **I/O device controller**: 디스크, 마우스와 같은 입출력 장치 관리. - **Bus** : 제어신호, 데이터, 주소 버스로 구성 ## Register : CPU 안에 있는 메모리. 1. CPU는 메모리에서 데이터를 레지스터로 읽어 옴. 2. 연산 결과를 레지스터에 저장 후 메모리에 저장 ### **Register의 종류** - **범용 레지스터** - **MBR** (Memory buffer register): 메모리에서 읽어온 데이터 저장 - **MAR** (Memory address register): 데이터의 메모리 주소 저장 - **stack pointer**: 메모리 내 스택 윗부분을 저장. - **특수 레지스터** : 프로세서의 연산 컨트롤을 위해 프로세서에 의해 사용됨. - **PC**: 다음 실행(fetch)할 명령어의 메모리 주소 저장 - **IR** (Instruction Register) - **PSW (Program Status Word)** : 코드 비트의 조건 (플래그) ex)우선순위, 모드 등 ### CPU pipeline : fetching, decoding, executing one  instruction at a time. 각각을 수행하는 유닛을 여러개 가짐. **Superscalar CPU**: 유닛 세트 여러 개 + Holding buffer **멀티스레드 CPU** : 하나의 코어가 여러 명령어를 동시에 처리 ### Interrupts : Suspends the normal sequence of execution. - 종류: 동기, 비동기 **인터럽트 처리 과정** 1. 인터럽트가 발생 2. 실행중인 유저 프로그램을 중단 3. **interrupt handler를** 실행. 4. 이후 실행중이던 프로그램으로 다시 돌아온다"
            +   "[example2] # 파일시스템 관리와 최적화 요약 ## 1. 파일 시스템의 기본 개념 ### (1) 파일 시스템의 필수 조건 - 많은 양의 정보를 저장할 수 있어야 함 - 프로세스가 종료된 후에도 정보가 유지되어야 함 - 여러 프로세스가 동시에 접근 가능해야 함 ### (2) 디스크의 구조와 관련 질문 - 디스크는 일렬로 배열된 고정 크기 블록으로 구성 - **주요 질문들:** - 정보를 어떻게 찾을 것인가? - 사용자가 다른 사용자의 데이터를 읽는 것을 어떻게 방지할 것인가? - 어떤 블록이 비어 있는지 어떻게 알 수 있을 것인가? ### (3) 파일과 파일 시스템 - 파일: 저장 장치에서 정보를 저장하는 기본 단위 - 바이트 배열 - 고유한 경로 이름 - 접근 제어 - 파일 시스템: 파일을 사용하는 서비스 제공하는 소프트웨어의 집합 ### (4) 파일 이름과 확장자 - 파일 확장자 예: - `.bak`: 백업 파일 - `.c`: C 소스 프로그램 - `.pdf`: PDF 파일 - `.zip`: 압축 아카이브 등 ## 2. 파일 구조와 타입 ### (1) 파일 구조 - 바이트 시퀀스 - 레코드 시퀀스 - 트리 구조 ### (2) 파일 타입 - 실행 파일, 아카이브 등 여러 타입 ### (3) 파일 속성 - **주요 파일 속성:** - 보호: 누가 어떤 방식으로 접근 가능한지 - 생성자, 소유자 등 다양한 속성 ### (4) 파일 접근 방식 - **순차 접근:** 파일의 앞에서부터 순차적으로 읽고 씀 - **직접 접근:** 임의 위치로 이동하여 읽고 씀 ### (5) 파일 공유 - 여러 프로세스가 파일을 동시에 열 수 있는가? - 파일 읽기/쓰기 권한 제어 ### (6) 파일 조작 관련 시스템 호출 - 생성, 삭제, 읽기, 쓰기, 열기, 닫기 등 주요 호출들 ## 3. 디렉토리 시스템 ### (1) 디렉토리의 개념 - 특수한 파일로 파일에 관한 정보 저장 ### (2) 계층적 디렉토리 시스템 - 디렉토리가 트리 구조로 구성됨 ### (3) 경로 이름 - **절대 경로:** 루트 디렉토리부터의 경로 - **상대 경로:** 현재 작업 디렉토리부터의 경로 ### (4) 디렉토리 조작 관련 시스템 호출 - 생성, 읽기, 삭제, 열기, 연결, 닫기, 연결 해제 등에 관련된 호출들 ## 4. 파일 시스템 할당 방식 ### (1) 연속 할당 - 파일 생성 시 연속된 블록을 할당 - 동적 파일 생성 및 삭제 시 외부 단편화 발생 가능 ### (2) 연쇄 할당 - 각 블록이 다음 블록에 대한 포인터 포함 - 외부 단편화 없음 - 동적 파일 생성 및 삭제에 적합 ### (3) 인덱스 할당 - 인덱스 블록이 파일의 데이터 블록 목록 가짐 - 외부 단편화 문제 없음 - 동적 생성 및 삭제에 적합 ## 5. 유닉스 파일 시스템 설계 - **i-node:** 각 파일의 속성과 블록 주소 저장 - **디스크 레이아웃:** 파티션 테이블, 부트 블록, 슈퍼블록, 자유 공간 관리, i-node, 루트 디렉토리 등"
            )

        elif subject == "COMPUTER_COMMUNICATION":
            example_summary = (
                "[example1] ## 1.4 delay, loss, throughput in networks ### Delay, loss 발생 이유 1. packet의 도착 속도 > output link 속도. 2. packet이 queue에 들어가게 됨. → delay 3. queue가 다 차있으면 packet 버려짐. → loss ### Delay의 네 가지 요소 - Nodal processing: 노드 처리 시간. ex) 비트 에러 체크 - Queueing delay: output link에서 전송 대기 시간. - transmission time: 데이터를 신호로 바꿔 내보내는 시간. packet length/link bandwidth - propagation delay: link위 전송 시간. length of physical link/propagation speed ### Throughput : 단위 시간당 송신자와 수신자 사이에 전송된 비트의 수 - end-end throughput: 더 작은 throughput에 의해 결정 됨. - bottleneck: throughput이 가장 작은 link. ## 1.5 protocol layers, service models ### Layer → 모듈화를 통해 유지보수 유리. 복잡한 시스템을 다루기에 좋음. ### **Internet protocol stack** - **application**: network application을 보조. ex) FTP, SMTP, HTTP - **transport**: proce - **network**:  source 부터 dest까지 datagram의 routing. ex) IP, routing protocol - **link**: 이웃하는 네트워크 구성요소 사이의 데이터 전달. ex) Ethernet, 802.110(WiFi) - **physical**: 전선의 비트들 전송 ### ISO/OSI reference model : 표준화 기구의 이상적인 모델 (7-layer) → *효율성이 떨어진다 !!* application layer와 transport layer 사이에 **presentation, session layer**가 존재. ### PDU (protocol data unit) - **header** : 중요한 정보 포함 - **L4 - PDU** : message L3-PDU : segment - **encapsulation**: head 붙이기 - **decapsulation**: 작게 쪼개기"
            )

        elif subject == "C_LANGUAGE":
            example_summary = (
                "[example1] # Ch4. 클래스와 객체I ## 4.1 객체 지향 프로그래밍이란? ### 객체 - 객체의 상태 - 객체의 동작 ### 객체 지향 프로그래밍 : 데이터와 함수를 하나의 덩어리로 묶어 생각하는 방법 ### 객체 지향 프로그래밍의 특징 1. 정보 은닉 2. 상속 3. 다형성 4. 추상화 ## 4.2 클래스와 객체 만들기 ### 클래스 : 객체에 대한 설계도 - 인스턴스: 클래스로부터 만들어지는 각각의 객 ### 클래스 작성 ex) ```java public class Circle{ public int radius; /*필드*/ public String color; public double getArea(){ /*메소드*/ return 3.14*radius*radius; } } ``` ### 객체 생성 1. 참조 변수 선언. 2. new 연산자로 객체 생성. 3. 객체의 필드, 메소드 사용. ex) ```java Circle obj; obj = new Circle(); obj.radius = 100; obj.color = \"blue\"; double area = obj.getArea(); ``` ### 참조 변수 : 객체를 참조할 때 사용되는 변수. ex) 배열, 클래스. 인터페이스"
            +   "[example2] # 포인터 요약 ## 1. 포인터의 기초 - **포인터란**: 주소를 가진 변수 - **변수의 주소**: 메모리에 저장되며, 바이트 단위로 액세스됨 - **포인터 선언**: ```c int *p;  // 정수를 가리키는 포인터 선언 ``` ## 2. 포인터의 연산 - **주소 연산자** `&`: 변수의 주소를 반환 - **간접 참조 연산자** ``: 포인터가 가리키는 곳의 내용을 반환 - **포인터 연산**: 증가, 감소, 덧셈, 뺄셈 - **형변환**: 필요한 경우 명시적으로 포인터의 타입을 변경 가능 ## 3. 포인터와 배열 - **포인터와 배열의 관계**: 배열 이름이 바로 포인터, 포인터는 배열처럼 사용 가능 - **배열 매개변수**: 배열의 이름은 포인터와 동일하게 동작 ```c void sub(int b[], int size); void sub(int *b, int size); ``` ## 4. 포인터와 함수 - **값에 의한 호출 (Call by Value)**: 함수로 복사본이 전달 - **참조에 의한 호출 (Call by Reference)**: 함수로 원본이 전달, C에서는 포인터로 구현 - **scanf 함수**: 변수에 값을 저장하기 위해 변수의 주소를 받음 - **여러 결과 반환**: 포인터를 사용해 여러 반환값 전달 가능 ```c int get_line_parameter(int x1, int y1, int x2, int y2, float *slope, float *yintercept); ``` ## 5. 포인터 사용의 장점 - 연결 리스트나 이진 트리 등 향상된 자료구조 생성 가능 - 함수 외부의 변수 값을 변경 가능 - 동적 메모리 할당 가능 ## 6. 포인터 사용시 주의점 - 초기화되지 않은 포인터 사용 금지 - NULL 포인터로 초기화 필요 - 포인터 타입과 변수 타입 일치 필요 ## 7. 예제 코드 - **포인터 기본 사용 예제**: ```c int i = 3000;           // 변수 i에 3000을 할당 int *p = &i;            // 포인터 p에 변수 i의 주소를 할당 printf(\"i=%d\n\", i);    // i의 값인 3000 출력 printf(\"&i=%u\n\", &i);  // i의 주소 출력 printf(\"p=%u\n\", p);    // 포인터 p가 가리키는 주소 출력 (i의 주소와 동일) printf(\"*p=%d\n\", *p);  // 포인터 p가 가리키는 변수의 값 출력 (i의 값인 3000 출력) ``` - **scanf 사용 예제**: ```c int x; scanf(\"%d\", &x); ```"
            )

        elif subject == "OBJECT_ORIENTED_PROGRAMMING":
            example_summary = (
                "[example1] # Ch6. 표준 출력 함수 ## 6.1 라이브러리 ### 라이브러리 : 지속적으로 업데이트가 필요한 함수들은 소스파일에 유지하고 나머지 함수는 라이브러리에 넣어서 관리. 기계어로 번역되어 있음. ### 라이브러리 파일 만드는 방법 1. 소스 파일 컴파일 2. 목적파일 프로그래머가 변환 3. 라이브러리 파일 완성 ## 6.2 라이브러리 사용 설명서, 헤더 파일 ### 헤더 파일 : 라이브러리에 있는 함수 원형을 미리 선언해 둔 파 ex) ```c int Add(int value1, int calue2); int Sub(int value1, int calue2); ``` ## 6.3 전처리기 ### 전처리기 : 프로그래머가 원하는 사항을 컴파일러에 직접 지시하는 문법 ### 전처리기 #include : 컴파일에 자신이 명시한 파일을 읽도록 지시 ex) ```c #include \"MyMath.h\" ``` ### 전처리기 #define : 상수나 명령문을 치환하는 문법 ex) ```c #define MAX_COUNT 3 ```"
            )


        sys_content_for_summary = (
                "You will receive the knowledge component (KC) and the contents of the corresponding learning materials."
                + "KC is a unit of learning concept. For example, in operating system subjects, process concepts, system calls, etc. can be KC. "
                + "You will summarize the given learning material in Markdown format for students studying operating system courses. "
                + "Summarize the entire content of the given course material. "
                + "Summary must be created based on the content of the study material."
                + "The summary should clearly illustrate the inclusion relationship to facilitate memorization and readability, and make appropriate use of bullet points. "
                + "kc and corresponding learning materials will be entered in the form of <page number>kc: learning material content, such as <0> Operating system definition: Operating system is ...., <14> Process concept: Process is, ...."
                + "Summarize the learning material and call the function get_summary. "
                + "Emphasize important content through techniques like bold formatting. "
                + "Subtopics should be numbered, and Keep in mind there should be a maximum of 7 subtopics, no more than that."
                + "You have to keep in mind that The entire summary must be made on one side of A4 paper."
                + "You must output the summary content in accordance with the flow and order of the study materials provided."
                + "You need to create a summary that will help students improve their learning efficiency right before the exam for this subject, so Keep in mind that omit unnecessary information and include only the really important information likely to be on the exam ."
                + "If the summary includes an output function such as 'print()' or 'printf()' or 'println()', Keep in mind that you have to provide the output result as a comment on the corresponding code line."
                + "Keep in mind that you must write summary in Markdown format."
        )

        user_content_for_summary = (
                "Summarize the following learning material for the operating system course in Korean. "
                + "Make it easy to memorize and be sure to format it nicely in Markdown. "
                + "Summarize the entire content of the given course material. "
                + "Emphasize important content through techniques like bold formatting. "
                + "Keep in mind that you must create Markdown format."
                + "[knowledge component and study material]: " + params["pdftxt"]
        )

        msg_for_summary = [
            {"role": "system", "content": sys_content_for_summary + example_summary},
            {"role": "user", "content": user_content_for_summary}
        ]

        return msg_for_summary

    def get_msg_for_kc(self, pdftxt, kc_list):
        sys_content = (
                "Given a page of study material and its associated Knowledge Component (KC) as input, you will classify the KC corresponding to the study material. "
                + "KC represents a unit of learning concept. "
                + "For example, in the subject of operating systems, KCs could include concepts like concept of threads, system calls, batch system scheduling etc. "
                + "KCs are accompanied by an ID. "
                + "For instance, if the concept on page 3 of a PDF is 'system calls' and its KC ID is 150, you should classify the KC ID of page 3 as 150. "
                + "Then, you will use the classified KCs to call the get_kc function. "
                + "The material will have contents like '<1>', '<2>' followed by the content of that page. "
                + "KC IDs and KCs will be provided in the format 'Operating System Definition 1   Operating System History 2.   System calls 3', where Learning Concept and KC ID. "
                + "You will receive the content of N pages. "
                + "Do not classify KCs as those not included in the given KCs."
                + "You have to keep in mind that you must classify the KC NOT NULL.")

        user_content = ("Give me the Knowledge Component IDs for all pages. "
                        + "The material will have contents like '<1>', '<2>' followed by the content of that page. "
                        + "KCs and KC IDs will be provided in the format '1 Operating System Definition 2 Operating System History', where KC ID and Learning Concept. "
                        + " [study material] " + pdftxt
                        + " [Knowledge Component] " + kc_list)

        msg = [
            {"role": "system", "content": sys_content},
            {"role": "user", "content": user_content}
        ]

        return msg

    def get_schema_for_choice(self):
        tools_for_choice = [
            {
                "type": "function",
                "function": {
                    "name": "get_problem",
                    "description": "Provide the multiple-choice question and answer.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prob_type": {
                                "type": "string",
                                "enum": ["BLANK", "MULTIPLE_CHOICE", "OX"],
                                "description": "The type of problem"
                            },
                            "kc_id": {
                                "type": "integer",
                                "description": "Knowlege component(KC) id corresponding to the page. KC represents a unit of learning concept.",
                            },
                            "kc": {
                                "type": "string",
                                "description": "Knowlege component(KC) corresponding to the question. KC represents a unit of learning concept. Write in Korean.",
                            },
                            "question": {
                                "type": "string",
                                "description": "The question of the quiz."
                            },
                            "options": {
                                "type": "object",
                                "properties": {
                                    "option_a": {
                                        "type": "string",
                                        "description": "The OPTION A of the question"
                                    },
                                    "option_b": {
                                        "type": "string",
                                        "description": "The OPTION B of the question"
                                    },
                                    "option_c": {
                                        "type": "string",
                                        "description": "The OPTION C of the question"
                                    },
                                    "option_d": {
                                        "type": "string",
                                        "description": "The OPTION D of the question"
                                    },
                                },
                                "required": ["option_a", "option_b", "option_c", "option_d"]
                            },
                            "answer": {
                                "type": "string",
                                "enum": ['a', 'b', 'c', 'd'],
                                "description": "The single letter of the CORRECT OPTION of the question."
                            },
                            "explanation": {
                                "type": "string",
                                "description": "The explanation about the quiz with up to 400 characters."
                            },
                        },
                        "required": ["prob_type", "kc", "question", "options", "answer", "explanation"],
                    }
                }
            }
        ]

        return tools_for_choice

    def get_schema_for_ox(self):
        tools_for_ox = [
            {
                "type": "function",
                "function": {
                    "name": "get_problem",
                    "description": "Provide the question and answer.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prob_type": {
                                "type": "string",
                                "enum": ["BLANK", "MULTIPLE_CHOICE", "OX"],
                                "description": "The type of problem"
                            },
                            "kc_id": {
                                "type": "integer",
                                "description": "Knowlege component(KC) id corresponding to the page. KC represents a unit of learning concept.",
                            },
                            "kc": {
                                "type": "string",
                                "description": "Knowlege component(KC) corresponding to the page. KC represents a unit of learning concept. Write in Korean.",
                            },
                            "question": {
                                "type": "string",
                                "description": "The question of quiz. It should be in the form of a proposition that can be evaluated as true or false. "
                            },
                            "answer": {
                                "type": "boolean",
                                "description": "The answer to the question, true or false"
                            },
                            "explanation": {
                                "type": "string",
                                "description": "The explanation about the quiz with up to 400 characters."
                            },
                        },
                        "required": ["prob_type", "kc", "question", "answer", "explanation"],
                    }
                }
            }
        ]

        return tools_for_ox

    def get_schema_for_blank(self):
        tools_for_blank = [
            {
                "type": "function",
                "function": {
                    "name": "get_problem",
                    "description": "Provide the question and content.",  # blank 내용 추가
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prob_type": {
                                "type": "string",
                                "enum": ["BLANK", "MULTIPLE_CHOICE", "OX"],
                                "description": "The type of problem"
                            },
                            "kc_id": {
                                "type": "integer",
                                "description": "Knowlege component(KC) id corresponding to the page. KC represents a unit of learning concept.",
                            },
                            "kc": {
                                "type": "string",
                                "description": "Knowlege component(KC) corresponding to the page. KC represents a unit of learning concept. Write in Korean.",
                            },
                            "question": {
                                "type": "string",
                                "description": "Provide a brief description of the content and instruct to fill in the blanks. e.g. For example, the following is code for process creation. Fill in the blanks."
                            },
                            "content": {
                                "type": "string",
                                "description": "Content with blanks. The number of blanks should be between 1 and 4. Blanks should be indicated with IDs in the format of ___ (1) ___, ___ (2) ___. Place three underscores before and after the blanks. IDs are assigned in order starting from 0, 1, 2, and so forth. The content can be an explanation of a concept or it can be programming code. Blanks should be created to verify understanding of important concepts."
                            },
                            "is_markdown": {
                                "type": "boolean",
                                "description": "Check if the content is written in Markdown format. If it is, fill with True; otherwise, fill with False."
                            },
                            "blanks": {
                                "type": "object",
                                "properties": {
                                    "blank_1": {
                                        "type": "string",
                                        "description": "The answer to the first blank."
                                    },
                                    "blank_2": {
                                        "type": "string",
                                        "description": "The answer to the second blank. If the second blank is empty, fill it with 'none'."
                                    },
                                    "blank_3": {
                                        "type": "string",
                                        "description": "The answer to the third blank. If the third blank is empty, fill it with 'none'."
                                    },
                                    "blank_4": {
                                        "type": "string",
                                        "description": "The answer to the fourth blank. If the fourth blank is empty, fill it with 'none'."
                                    },
                                },
                                "required": ["blank_1", "blank_2", "blank_3", "blank_4"]
                            },
                            "explanation": {
                                "type": "string",
                                "description": "The explanation about the quiz with up to 400 characters."
                            },
                        },
                        "required": ["prob_type", "kc", "question", "content", "blanks", "explanation"],
                    }
                }
            },
        ]

        return tools_for_blank

    def get_schema_for_summary(self):
        tools_for_summary = [
            {
                "type": "function",
                "function": {
                    "name": "get_summary",
                    "description": "Provide summary of the given learning material in Markdown format.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "Summarized the given learning material in Markdown format. The summary should clearly illustrate the inclusion relationship to facilitate memorization and readability, and make appropriate use of bullet points. And summary is Korean. # Concept of Operating Systems - **Definition:** Operating "
                            },
                        },
                        "required": ["summary"],
                    }
                }
            }
        ]

        return tools_for_summary

    def get_schema_for_kc(self):
        tools_for_kc = [
            {
                "type": "function",
                "function": {
                    "name": "get_kc",
                    "description": "Provide the knowledge component ID corresponding to the page",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "page_number": {
                                "type": "integer",
                                "description": "Page number, e.g. 1, 2",
                            },

                            "kc": {
                                "type": "string",
                                "description": "Knowlege component(KC) id corresponding to the page. KC represents a unit of learning concept. Write in Korean.",
                            },

                            "kc_id": {
                                "type": "integer",
                                "description": "Knowlege component(KC) id corresponding to the page. KC represents a unit of learning concept. For example, if the concept on page 3 is 'system calls' and if 'system calls' KC ID is 150, kc_id is 150."
                                               + "KCs and KC IDs will be provided in the format 'Operating System Definition 0     Operating System History 1     System calls 2', where Learning Concep and KC ID. "
                                               + "Then, 'Operating System Definition''s KC ID is 0, 'Operating System History''s KC ID is 1, 'System calls''s KC ID is 2, NOT NULL.",
                            }

                        },
                        "required": ["page_number", "kc_id", "kc"],
                    }
                }
            }
        ]
        return tools_for_kc
