// FileUpload.tsx
import React, { useCallback, useState, useEffect } from "react";
import { Button, CircularProgress, Box } from "@mui/material";
import { useDropzone } from "react-dropzone";
import styled from "styled-components";
import { uploadPdfFile } from "../api/axios";
import { useNavigate } from "react-router-dom";

const DropzoneArea = styled.div<{ isDragActive?: boolean }>`
  border: 2px dashed #eeeeee;
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: "Pretendard Variable";
  font-display: swap;
  src: local("Pretendard Variable"),
    url("./PretendardVariable.ttf") format("ttf");
  height: 500px; /* 원하는 높이로 조정 */
  background-color: ${(props) =>
    props.isDragActive ? "#e0e0e0" : "transparent"};
`;

interface FileUploadProps {
  token: string; // JWT 토큰을 props로 받습니다.
  selectedSubject: string | null;
}

const FileUpload: React.FC<FileUploadProps> = ({ token, selectedSubject }) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "loading" | "done">(
    "idle"
  );
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [pdfId, setPdfId] = useState<number>(0);
  const [totalPageCount, setTotalPageCount] = useState<number>(0);
  const generateQuizNum: string = "1";
  const navigate = useNavigate();

  const handleSubmit = useCallback(async () => {
    if (selectedFiles.length === 0) return;
    setUploadStatus("loading");

    try {
      const data = await uploadPdfFile(token, selectedFiles, selectedSubject);
      console.log("File uploaded successfully", data);
      setUploadedFileName(data.body.data.uploadFileName); // 예시 응답에서 파일 이름을 가져온다고 가정
      setPdfId(data.body.data.pdfId);
      setTotalPageCount(data.body.data.totalPageCount);

      setUploadStatus("done");
    } catch (error) {
      console.error("Upload failed", error);
      setUploadStatus("idle"); // 실패 시 상태를 초기화
    }
  }, [selectedFiles, token]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setSelectedFiles(acceptedFiles);
    handleSubmit(); // 파일이 드롭될 때 handleSubmit 호출
  }, []); // 의존성 배열에 handleSubmit 추가

  useEffect(() => {
    if (selectedFiles.length > 0) {
      handleSubmit();
    }
  }, [selectedFiles, handleSubmit]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const { ref, ...rootProps } = getRootProps();

  return (
    <DropzoneArea ref={ref} {...rootProps} isDragActive={isDragActive}>
      <input {...getInputProps()} accept=".pdf" />
      {uploadStatus === "loading" ? (
        <CircularProgress />
      ) : uploadStatus === "done" ? (
        <>
          <img src="pdf_icon.svg" alt="" style={{ marginTop: "140px" }} />
          <p style={{ marginBottom: "140px" }}>{`${uploadedFileName}`}</p>
          <Box
            sx={{
              display: "flex", // 이 줄을 추가하여 flexbox를 활성화합니다.
              justifyContent: "center", // 버튼들을 가운데 정렬합니다. 필요에 따라 'flex-start', 'flex-end', 'space-between' 등으로 변경 가능합니다.
              alignItems: "center", // 버튼들을 세로 방향으로 중앙에 위치시킵니다.
              m: 1, // 마진을 추가합니다. 필요에 따라 조정하세요.
            }}
          >
            <Button
              sx={{
                color: "white",
                background: "gray",
                borderRadius: "16px",
                width: "150px",
                ":hover": { background: "#ffc450", color: "black" },
              }}
              onClick={(event) => {
                event.stopPropagation(); // 이벤트 버블링을 중지합니다.
                navigate("/makequiz", {
                  state: {
                    uploadedFileName,
                    pdfId,
                    totalPageCount,
                    selectedSubject,
                    generateQuizNum,
                  },
                });
              }}
            >
              퀴즈 생성하기
            </Button>
          </Box>
        </>
      ) : (
        <>
          {isDragActive ? (
            <p>파일을 여기에 놓으세요...</p>
          ) : (
            <p>파일을 드래그하거나 클릭하여 선택하세요.</p>
          )}
        </>
      )}
    </DropzoneArea>
  );
};

export default FileUpload;
