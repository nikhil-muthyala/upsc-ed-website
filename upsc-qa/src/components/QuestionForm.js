// src/components/QuestionForm.js
import React, { useState } from "react";

function QuestionForm({ onReceiveAnswer }) {
    const [question, setQuestion] = useState("");
    const [format, setFormat] = useState("short");

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Simulate a backend call
        const response = await simulateBackendResponse(question, format);
        onReceiveAnswer(response);
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Enter Your Question:
                <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Type your question here..."
                />
            </label>
            <label>
                Choose Answer Format:
                <select value={format} onChange={(e) => setFormat(e.target.value)}>
                    <option value="short">Short Explanation</option>
                    <option value="detailed">Detailed (150-200 words)</option>
                    <option value="summary">Summary</option>
                </select>
            </label>
            <button type="submit">Get Answer</button>
        </form>
    );
}

// Simulated backend response function
async function simulateBackendResponse(question, format) {
    let answer = "";
    if (format === "short") {
        answer = "This is a short explanation.";
    } else if (format === "detailed") {
        answer = "This is a detailed answer with an introduction, body, and conclusion.";
    } else {
        answer = "This is a summary answer.";
    }

    const relatedLinks = [
        { title: "Related Article 1", url: "https://example.com/article1" },
        { title: "Related Article 2", url: "https://example.com/article2" }
    ];

    await new Promise(resolve => setTimeout(resolve, 1000));

    return { answer, relatedLinks };
}

export default QuestionForm;


