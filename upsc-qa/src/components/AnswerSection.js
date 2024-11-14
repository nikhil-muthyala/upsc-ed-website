// src/components/AnswerSection.js
import React from "react";

function AnswerSection({ answer, relatedLinks }) {
    return (
        <div className="answer-section">
            <h2>Answer</h2>
            <p>{answer}</p>

            <h3>Related Reading Material</h3>
            <ul>
                {relatedLinks.map((link, index) => (
                    <li key={index}>
                        <a href={link.url} target="_blank" rel="noopener noreferrer">
                            {link.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default AnswerSection;
