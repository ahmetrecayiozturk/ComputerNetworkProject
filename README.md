# 🎓 Quiz Competition Program (Socket-Based)

This project is a quiz competition application developed using socket programming and supports multi-process/client management. The code is written in Python and includes a GUI client (contestant), the main server (quiz controller), and a joker server (for lifeline features).

## Components

- **clientwithui.py**: Tkinter-based graphical interface client for contestants.
- **program.py**: Main quiz server. Sends questions, receives answers, and communicates with the joker server for lifelines.
- **joker.py**: Joker server. Provides answers for "Audience" and "Fifty-Fifty" lifelines.
- **question.py**: Definition of the Question class and storage for question data.

## Setup

> **Note:** This code is designed to run on localhost (127.0.0.1) with Python 3.

1. Make sure you have Python 3.x installed (Tkinter comes by default).
2. Place all files in the same directory.

## Run Order

To ensure proper communication between the components, **start them in the following order**:

1. **Start joker.py**  
   ```bash
   python joker.py
   ```
   - The joker server will start and wait for connections.

2. **Start program.py**  
   ```bash
   python program.py
   ```
   - The main quiz server will start and wait for a contestant to connect.

3. **Start clientwithui.py**  
   ```bash
   python clientwithui.py
   ```
   - The contestant GUI will open and connect to the server.

> **WARNING:**  
> Do **not** start `joker.py` more than once!  
> You must always follow this order:  
> **First** `joker.py` → **then** `program.py` → **then** `clientwithui.py`

## How to Play

- The contestant selects an answer (A/B/C/D) for each question displayed in the GUI.
- There are two lifelines:
  - **Audience Lifeline (S):** Shows audience probability for each choice.
  - **Fifty-Fifty Lifeline (Y):** Eliminates two incorrect options.
- When a lifeline is used, information is shown in the GUI and it cannot be used again.
- After each answer, you'll see if you were correct and your prize (according to the prize table).
- The quiz ends immediately on a wrong answer or after the last question.

## Code Flow

- `clientwithui.py`:  
  Connects to the server, displays questions, sends answers and lifeline requests.
- `program.py`:  
  Sends questions one by one, receives answers, connects to `joker.py` when lifelines are used, and sends results back to the client.
- `joker.py`:  
  Processes lifeline requests and returns either audience results or two eliminated options.

## File Details

- **question.py**
  ```python
  class Question:
      def __init__(self, question, options, correct_answer, joker_type_s, joker_type_y):
          self.question = question
          self.options = options
          self.correct_answer = correct_answer
          self.joker_type_s = joker_type_s 
          self.joker_type_y = joker_type_y
  ```
- Example questions and prize table are defined in `program.py` and `joker.py`.

## Dependencies

- Python 3.x
- Tkinter (comes with Python 3)
- Standard `socket` module

---

## Wireshark Analysis

Below you can find example Wireshark screenshots showing the TCP packets exchanged during the quiz application's operation. Each image demonstrates a different step in the client-server communication, including question delivery, answer processing, lifeline requests, and quiz end notifications.

### Example Packet Analyses

#### 1. Question and Answer Packet
This packet shows the transfer of a question from the server to the client, and the subsequent answer sent back from the client.
<img width="1500" height="474" alt="image" src="https://github.com/user-attachments/assets/86cd96bb-9523-4412-a775-fe5a613710c5" />
<img width="1500" height="457" alt="image" src="https://github.com/user-attachments/assets/1937ab60-8401-4714-a3a9-c8f7763b99de" />


#### 2. Audience Joker Request Packet (Joker Server)
This packet demonstrates the audience lifeline request being processed by the joker server and the response sent back.
<img width="1500" height="721" alt="image" src="https://github.com/user-attachments/assets/549bb771-3b44-4f1a-a5c4-7a2d651d2294" />


#### 3. Program Exit
This image shows the end of the program.
<img width="1500" height="439" alt="image" src="https://github.com/user-attachments/assets/fc580c7d-b2cc-474c-8efa-25d278cc956d" />

> Each screenshot displays the relevant TCP stream at the top, with detailed packet content and raw data (hex + ASCII) at the bottom. These analyses help you understand how the protocol works at the transport layer and how the application data is packed and transmitted.

---

## Contact

For bug reports or suggestions, please contact the project owner.
