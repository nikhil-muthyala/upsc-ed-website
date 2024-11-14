// src/App.js
import React, { useState } from "react";
import "./App.css";
import QuestionForm from "./components/QuestionForm";
import AnswerSection from "./components/AnswerSection";

function App() {
    const [answer, setAnswer] = useState(null);
    const [relatedLinks, setRelatedLinks] = useState([]);

    const handleAnswerResponse = (response) => {
        setAnswer(response.answer);
        setRelatedLinks(response.relatedLinks);
    };

    return (
        <div className="App">
            <h1>UPSC Question Answer System</h1>
            <QuestionForm onReceiveAnswer={handleAnswerResponse} />
            {answer && <AnswerSection answer={answer} relatedLinks={relatedLinks} />}
        </div>
    );
}

export default App;
