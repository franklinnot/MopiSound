import getFilename from "./get-filename";

export default async function createFile(response: Response): Promise<boolean> {
    try{
        const blob = await response.blob();
        let filename = getFilename(response.headers.get("content-disposition"));
      
        if (!filename) {
          filename = "mopi";
        }
      
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(downloadUrl);
        return true;
    }
    catch{
        return false;
    }
}
