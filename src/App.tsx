import { useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";

function App() {
  useEffect(() => {
    invoke("init");
  }, []);

  return (
    <div className="flex flex-col items-center justify-center pt-[10vh]">
      <h1>Menubar App</h1>
      <p>Your content goes here...</p>
    </div>
  );
}

export default App;