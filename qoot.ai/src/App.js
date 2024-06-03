import { Routes, Route } from "react-router-dom";
import Marathi from "./pages/Marathi";
import Eng_input from "./pages/Eng_input";
import English from "./pages/English";
import Home from "./pages/Home";
import "./App.css";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/marathi" element={<Marathi />} />
        <Route path="/input_eng" element={<Eng_input />} />
        <Route path="/english" element={<English />} />
      </Routes>
    </div>
  );
}

export default App;