const express = require("express");
const cors = require("cors");
const rateLimit = require("express-rate-limit");
const bodyParser = require("body-parser");
const { config } = require("dotenv");
const { OpenAI } = require("openai");

config();

const app = express();
const PORT = process.env.PORT || 3000;

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Rate Limiting: 5 requests per IP per day
const limiter = rateLimit({
  windowMs: 24 * 60 * 60 * 1000, // 1 day
  max: 500,
  message: "Rate limit exceeded. Only 500 requests per day allowed.",
});

app.use(limiter);

app.get("/", (req, res) => {
  res.json({
    message:
      "Welcome to the ATS Checker API. Use POST / to check ATS compatibility.",
  });
});

app.post("/", async (req, res) => {
  const { resume, job_description } = req.body;

  const system_prompt = process.env.SYSTEM_PROMPT.trim();

  const user_content = `Job Description:\n${job_description}\n\nResume:\n${resume}`;

  try {
    const response = await client.chat.completions.create({
      model: process.env.OPENAI_MODEL,
      messages: [
        { role: "system", content: system_prompt },
        { role: "user", content: user_content },
      ],
      temperature: 0.4,
    });

    const ai_reply = response.choices[0].message.content;
    res.json({ result: ai_reply });
  } catch (err) {
    console.error("OpenAI Error:", err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`ATS Checker API is running on http://localhost:${PORT}`);
});
