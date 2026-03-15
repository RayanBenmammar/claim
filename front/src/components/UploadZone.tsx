import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

export function UploadZone() {
  const [file, setFile] = useState<File | null>(null);
  const [inputClass, setInputClass] = useState("file-input file-input-primary");

  const validateFile = (file: File) => {
    const allowedTypes = ["application/pdf", "image/png", "image/jpeg"];
    return allowedTypes.includes(file.type);
  };

  const onFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputClass("file-input file-input-primary");
    setFile(null);
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      if (!validateFile(file)) {
        setInputClass("file-input file-input-error");
        return;
      }
      setFile(file);
    }
  };
  const mutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      const apiUrl = import.meta.env.VITE_API_URL;
      const response = await fetch(`${apiUrl}/documents`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("File upload failed");
      }
      return response.json();
    },
  });

  return (
    <div className="hero bg-base-200 min-h-screen">
      <div className="hero-content text-center">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold">Hello Claim</h1>
          <fieldset className="fieldset">
            <legend className="fieldset-legend">Upload your document</legend>
            <input
              id="input-file"
              type="file"
              className={inputClass}
              accept="application/pdf,image/png,image/jpeg"
              onChange={onFileUpload}
            />
          </fieldset>
          <button
            className="btn btn-primary"
            disabled={!file}
            onClick={() => file && mutation.mutate(file)}
          >
            Upload
          </button>
          <div>
            {mutation.isPending ? (
              "Uploading..."
            ) : mutation.isError ? (
              <div>An error occured: {mutation.error.message}</div>
            ) : mutation.isSuccess ? (
              <div>File uploaded successfully!</div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}
