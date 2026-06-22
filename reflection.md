# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
1) The secret number is outside the range
2) New Game does not work after the game is over
3) The History appends the previous number guessed, not the most recent
4) New Game does not restart history or score but resets attemps and makes a new secret number
5) The Range of Numbers appear to be 1 to 100 for every difficulty
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| guess 30 | Hint: Go Higher | Hint: Go Lower | Hints are opposite |
| guess 40 | history appends with 40| history appends with 30| history appends with previous input|
| press new game when game is over| game/score resets | nothing happens| |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
When exploring the bug where restart doesn't function correctly, claude found two restart bugs in app.py. Status was never reset after a class and clicking new game keep sstatus as "won" or "lost". Therefore the game never runs again.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The new game button rerolls the secret number from 1-100 regardless of difficulty chosen. Claude suggested to fix New Game to use the difficulty range (core bug), fix the prompt text to show the actual range, and rebalance Hard so its range is larger than Normal.
Even though this is probably correct, it is not exactly a bug because it is what the developer intentionally designed it to do. Therefore even doesn't make sense logically, it functions correctly.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I generated pytest cases to test whether the bug was fixed. I also ran the app myself and made sure the feature was functioning correctly.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I opened the app, played a game until completion then tried to restart the game. I played several games to make sure the restart game functionality worked correctly.
- Did AI help you design or understand any tests? How?
Yes, AI helped me by explaining what each of the test cases tested. For example TestRestartResetsStatus covers if status goes back to "playing" after a win or loss. Another case it tested was TestRestartClearsHistory. This checked if history is cleared after each restart.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit runs a python script everytime a user intereacts with the app. It also gives you session states as a dictionary to store values between reruns.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
I like the idea of using AI to generate test cases so I will employ that strategy to future projects.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
I will ask it to implement comments to the code so I can see the changes it made.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I would say this lesson only reconfirmed my general view of how AI can be used in coding projects. It is a powerful tool that needs supervision from a programmer so that the functionality being implemented is something that makes sense.