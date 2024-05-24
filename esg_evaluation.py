import os
import openai
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key
MODEL = "gpt-4"



from openai import OpenAI

client = OpenAI()

print(os.environ.get("OPENAI_API_KEY"))

def get_esg_evaluation_with_api(user_responses):
    prompt = """
    ESG guidelines based Questions :-

    question1: Governance Structure: Rate the effectiveness of your organization's governance structure in overseeing ESG issues, including the role of the board.
    question2: Processes and Controls: Evaluate the adequacy of the processes and controls in place to monitor and manage ESG risks and opportunities.
    question3: ESG Integration: How effectively does your company's strategy integrate ESG considerations?
    question4: Long-term ESG Targets: Rate the clarity and ambition of the long-term targets your company has set to address sustainability issues.
    question5: Risk Identification Processes: Assess how effectively your company identifies, assesses, prioritizes, and manages ESG risks.
    question6: Integration into Overall Risk Framework: How well are ESG risks integrated into the overall risk management framework?
    question7: ESG Metrics Tracking: Evaluate the relevance and comprehensiveness of the ESG metrics your company tracks and reports.
    question8: Use of Metrics in Performance Assessment: How effectively are these metrics used to assess performance against ESG targets?
    question9: Adherence to Standards: Rate how well your company's sustainability reporting follows recognized frameworks and standards.
    question10: Accuracy and Reliability: Assess the accuracy and reliability of your company's ESG reporting.
    question11: Engagement Effectiveness: Evaluate how effectively your company engages with stakeholders on sustainability issues.
    question12: Feedback Mechanisms: Rate the effectiveness of the feedback mechanisms in place for stakeholders to raise concerns or suggestions.
    question13: Implementation of ESG Initiatives: Rate the effectiveness of the ESG initiatives implemented over the past year.
    question14: Future ESG Performance Improvement: How well does your company plan to improve its ESG performance moving forward?
    question15: Compliance with Regulations: Assess your company's compliance with local and international ESG-related regulations.
    question16: Alignment with ESG Frameworks: Rate how well your ESG practices align with frameworks such as IFRS S1 and SASB standards.
    question17: Innovation in Sustainability Efforts: Evaluate the level of innovation in your company's sustainability efforts.
    question18: Promotion of Continuous Improvement: How effectively does your company promote continuous improvement in its ESG practices?

    Categorization of each question :-

    1. Governance :- questions - question1, question2
    2. Strategy :- questions - question3, question4
    3. Risk Management :- questions - question5, question6
    4. Metrics and Targets :- questions - question7, question8
    5. Reporting and Disclosure :- questions - question9, question10
    6. Stakeholder Engagement :- questions - question11, question12
    7. Performance Review :- questions - question13, question14
    8. Compliance and Alignment :- questions - question15, question16
    9. Innovation and Continuous Improvement :- questions - question17, question18

    Rating Marking Scheme :-

    Rating 0-100 :-
        Result :- Developing
        Message :-  Your company is beginning to develop ESG objectives and working to operationalize them throughout the organization.

    Rating 100-150 :-
        Result :- Integrated
        Message :- Your company has established ESG objectives and integrated them into operations. There is opportunity to expand your ESG program to lead in the market.

    Rating 150-200 :-
        Result :- Optimised
        Message :- Your ESG program is well-defined and optimized throughout your organization. ESG is embedded in all aspects of decision-making.

    You are an ESG analyst. You are being provided with ESG guidelines based Questions, Categorization of each question, Rating Marking Scheme. For each question, the user will provide a response as an integer from 1-10 as a dictionary. A sample dictionary is provided as following
    {"question1":"1","question2":"5","question3":"2","question4":"1","question5":"1","question6":"2","question7":"1","question8":"2","question9":"1","question10":"2","question11":"1","question12":"2","question13":"4","question14":"5","question15":"4","question16":"7","question17":"1","question18":"2"}
    You have to perform two tasks.
    First, Classify the result as per the marking scheme, and give the result and the overall message.
    Second, as per the response you received for each question, and using the categorization of questions, generate an output where you give a list of categories(only 5 categories in descending order of the seriousness of the problem of the category) that the company needs to work upon from the categories provided in Categorization of each question section, and for each category, you need to write in 50-100 words whats wrong and give the roadmap to improve.
    Your output should have
    Result Classification:
    Top 5 Categories for Improvement and Roadmap:
    """

    user_prompt = """
        User Responses:
        """ + str(user_responses)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model=MODEL,
        seed=42,
        max_tokens=1500,
        temperature=0.7,
    )

    return chat_completion.choices[0].message.content
