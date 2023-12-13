import tkinter as tk
import random
from questions import questions
from tkinter import messagebox

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Maker")  # Set an empty title to hide default title bar
        self.root.geometry("400x300")  # Adjust the window size as needed

        # Creating a frame to simulate a custom title bar
        self.title_bar = tk.Frame(root, height=40, bg="lightgray")  # Adjust height as needed
        self.title_bar.pack(fill=tk.X)

        # Loading the image for the icon
        try:
            icon = tk.PhotoImage(file="thd.png")  # Replace 'thd.png' with your actual icon file
        except tk.TclError as e:
            print("Image not found:", e)
            icon = None

        # Displaying the icon on the canvas
        if icon:
            icon_label = tk.Label(self.title_bar, image=icon, bg="lightgray")
            icon_label.image = icon  # Keeping a reference to the image to prevent garbage collection
            icon_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Initialize variables
        self.questions = questions  # List to hold all questions
        self.current_question = 0  # Track current question index
        self.score = 0
        self.total_questions = 0
        self.timer = None
        self.time_left = 0

        # GUI components
        self.login_frame = tk.Frame(root)
        self.login_frame.pack()

        self.name_label = tk.Label(self.login_frame, text="Enter Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.login_frame)
        self.name_entry.pack()

        self.surname_label = tk.Label(self.login_frame, text="Enter Surname:")
        self.surname_label.pack()

        self.surname_entry = tk.Entry(self.login_frame)
        self.surname_entry.pack()

        self.id_label = tk.Label(self.login_frame, text="Enter Student ID:")
        self.id_label.pack()

        self.id_entry = tk.Entry(self.login_frame)
        self.id_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

        self.timer_label = tk.Label(self.root, text="")
        self.timer_label.pack()

        self.question_frame = tk.Frame(root)
        self.question_frame.pack_forget()  # Hide the question frame initially

        # Load questions and start the quiz
        self.load_questions()
        self.show_login()

        # Exit button
        self.exit_button = tk.Button(self.root, text="Exit Quiz", command=self.end_current_quiz)

        # Exit button initially hidden
        self.exit_button = tk.Button(self.root, text="Exit Quiz", command=self.end_current_quiz)
        self.exit_button.pack_forget()  # Hide the exit button initially

        self.retake_button = tk.Button(self.root, text="Retake Quiz", command=self.retake_quiz)
        self.retake_button.pack()
        self.retake_button.pack_forget()  # Hide the retake button initially

    def show_login(self):
        # Show only login elements
        self.login_frame.pack()
        self.question_frame.pack_forget()

    def validate_input(self):
        try: 
            name = self.name_entry.get().strip()
            surname = self.surname_entry.get().strip()
            student_id = self.id_entry.get().strip()

            if not name or not surname or not student_id:
                raise ValueError("Please fill in all fields.")
        
            # Validate name and surname (allowing only alphabetic characters and spaces)
            if not name.isalpha() or not surname.isalpha():
                raise ValueError("Name and surname should contain only letters.")

            # Validate student ID (assuming it should contain only digits)
            if not student_id.isdigit():
                raise ValueError("Student ID should contain only numbers.")
            return True

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
            return False
    

    def login(self):
        if self.validate_input():
            self.hide_login()  # Move forward with valid inputs
        else:
            c = 0    # Inputs are invalid, stay on the login screen

    def hide_login(self):
        self.login_frame.pack_forget()  # Hide login elements
        self.question_frame.pack()  # Show question frame
        self.start_quiz()  # Display the first question after login
        self.exit_button.pack()  # Show the exit button after login

    def load_questions(self):
        self.questions = questions  # Load questions

        # Shuffle choices for each question
        for question in self.questions:
            if "choices" in question:
                random.shuffle(question["choices"])

    def start_quiz(self):
        self.total_questions = len(self.questions)
        self.shuffle_questions()  # Randomize the order of questions
        self.show_question()

    def shuffle_questions(self):
        random.shuffle(self.questions)

    def show_question(self):
        if hasattr(self, "current_question_label"):
            self.current_question_label.pack_forget()
            if hasattr(self, "current_choices_frame"):
                self.current_choices_frame.pack_forget()
            if hasattr(self, "previous_button"):
                self.previous_button.pack_forget()
            if hasattr(self, "next_button"):
                self.next_button.pack_forget()

        if self.current_question < self.total_questions:
            current_question_data = self.questions[self.current_question]
            # Clear previous question elements if they exist
            # ...

            # Display the question
            self.current_question_label = tk.Label(self.root, text=current_question_data["question"])
            self.current_question_label.pack()

            # Check if 'choices' key exists in the question data
            if "choices" in current_question_data:
                self.current_choices_frame = tk.Frame(self.root)
                self.current_choices_frame.pack()
                for choice in current_question_data["choices"]:
                    choice_button = tk.Button(self.current_choices_frame, text=choice, command=lambda ch=choice: self.submit_answer(ch))
                    choice_button.pack()

            # Start countdown timer for the question
            self.time_left = 10  # Set the time per question (adjustable)
            self.start_timer()

            # Display the score for the current question
            score_text = f"Score: {self.score} / {self.total_questions}"
            if hasattr(self, "score_label"):
                self.score_label.configure(text=score_text)
            else:
                self.score_label = tk.Label(self.root, text=score_text)
                self.score_label.pack()

            # Navigation buttons for moving between questions
            if self.current_question > 0:
                self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_question)
                self.previous_button.pack()

            if self.current_question < self.total_questions - 1:
                self.next_button = tk.Button(self.root, text="Next", command=self.next_question)
                self.next_button.pack()

        else:
            self.end_quiz()

    def start_timer(self):
        if self.timer is None:  # Start the timer only if it's not running
            self.update_timer()

    def update_timer(self):
        if self.time_left >= 0:
            elapsed_time = 10 - self.time_left
            remaining_time = max(0, 10 - elapsed_time)
            self.timer_label.config(text=f"Timer: {remaining_time}")
            self.timer = self.root.after(1000, self.update_timer)
            self.time_left -= 1
        else:
            self.next_question()

    def submit_answer(self, choice):
        current_question_data = self.questions[self.current_question]

        # Check the answer for MCQ or True/False
        correct_answer = current_question_data["answer"]
        if choice == correct_answer:
            self.score += 1  # Increase score for correct answer

        self.clear_gui_elements()  # Clear GUI elements for the current question
        self.next_question()

    def clear_gui_elements(self):
        a = 0

    def previous_question(self):
        # Move to the previous question
        self.current_question -= 1
        self.clear_timer()  # Reset the timer before moving to the previous question
        self.show_question()

    def next_question(self):
        # Move to the next question
        self.current_question += 1
        self.clear_timer()  # Reset the timer before moving to the next question
        self.show_question()

    def clear_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

    def save_results(self):
        try:
            # Get the student ID
            student_id = self.id_entry.get().strip()

            # Create the file name based on the student ID
            filename = f"results-{student_id}.txt"

            # Open the file in append mode to add the user's score
            with open(filename, 'a') as file:
                file.write(f"Student ID: {student_id}\n")
                file.write(f"Score: {self.score}/{self.total_questions}\n")
                file.write("\n")

        except Exception as e:
            messagebox.showerror("File Error", f"Error saving results: {str(e)}")

    def end_quiz(self):
        correct_answers = 0
        total_questions = len(self.questions)

        for question in self.questions:
            if question["answer"] == question["choices"][0]:  # Assuming the first choice is the correct answer
                correct_answers += 1

        percentage = (self.score / total_questions) * 100
        result = "Passed" if percentage >= 50 else "Failed"

        report = f"Correct Answers: {correct_answers}/{total_questions}\n"
        report += f"Achieved Percentage: {percentage:.2f}%\n"
        report += f"Result: {result}"

        try:
            # Display quiz ended message
            messagebox.showinfo("Quiz Ended", "The quiz has ended.")
            # Display quiz report
            messagebox.showinfo("Quiz Report", report)
            # Save results to file
            self.save_results()
            # Show retake button after the quiz ends
            self.retake_button.pack()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def retake_quiz(self):
        # Reset quiz state for a new user or retake
        self.current_question = 0
        self.score = 0
        self.timer_label.config(text="")  # Clear timer label
        self.retake_button.pack_forget()  # Hide the retake button
        self.show_login()  # Show login elements to start again


    def end_current_quiz(self):
        # Confirm before ending the quiz
        confirm = messagebox.askyesno("Warning", "Are you sure you want to end the quiz?")
        if confirm:
            self.root.destroy()  # Close the quiz window
        else:
            pass  # User chose not to end the quiz, continue

    # ... Other methods


def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()



