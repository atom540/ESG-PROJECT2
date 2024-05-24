import streamlit as st
import json
from esg_evaluation import get_esg_evaluation_with_api 

sections = {
    "Section 1": [
        "Governance Structure: Rate the effectiveness of your organization's governance structure in overseeing ESG issues, including the role of the board.",
        "Processes and Controls: Evaluate the adequacy of the processes and controls in place to monitor and manage ESG risks and opportunities.",
        "ESG Integration: How effectively does your company's strategy integrate ESG considerations?",
        "Long-term ESG Targets: Rate the clarity and ambition of the long-term targets your company has set to address sustainability issues.",
        "Risk Identification Processes: Assess how effectively your company identifies, assesses, prioritizes, and manages ESG risks."
    ],
    "Section 2": [
        "Integration into Overall Risk Framework: How well are ESG risks integrated into the overall risk management framework?",
        "ESG Metrics Tracking: Evaluate the relevance and comprehensiveness of the ESG metrics your company tracks and reports.",
        "Use of Metrics in Performance Assessment: How effectively are these metrics used to assess performance against ESG targets?",
        "Adherence to Standards: Rate how well your company's sustainability reporting follows recognized frameworks and standards.",
        "Accuracy and Reliability: Assess the accuracy and reliability of your company's ESG reporting."
    ],
    "Section 3": [
        "Engagement Effectiveness: Evaluate how effectively your company engages with stakeholders on sustainability issues.",
        "Feedback Mechanisms: Rate the effectiveness of the feedback mechanisms in place for stakeholders to raise concerns or suggestions.",
        "Implementation of ESG Initiatives: Rate the effectiveness of the ESG initiatives implemented over the past year.",
        "Future ESG Performance Improvement: How well does your company plan to improve its ESG performance moving forward?",
        "Compliance with Regulations: Assess your company's compliance with local and international ESG-related regulations."
    ],
    "Section 4": [
        "Alignment with ESG Frameworks: Rate how well your ESG practices align with frameworks such as IFRS S1 and SASB standards.",
        "Innovation in Sustainability Efforts: Evaluate the level of innovation in your company's sustainability efforts.",
        "Promotion of Continuous Improvement: How effectively does your company promote continuous improvement in its ESG practices."
    ]
}


st.set_page_config(page_title="ESG_SERVY")

def display_questions(section_name, questions):
    responses = st.session_state.responses.get(section_name, {})
    for i, question in enumerate(questions):
        key = f"{section_name}_{i}"
        response = responses.get(question, 0) 
        response = st.number_input(question, min_value=0, max_value=10, step=1, format="%d", key=key, value=response)
        responses[question] = response
    st.session_state.responses[section_name] = responses  # Update session state with current responses
    return responses


if 'section' not in st.session_state:
    st.session_state.section = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {section: {} for section in sections}
def main():
    section_names = list(sections.keys())
    total_sections = len(section_names)

    current_section = st.session_state.section
    section_name = section_names[current_section]
    st.title(section_name)

    responses = display_questions(section_name, sections[section_name])

    
    st.session_state.responses[section_name] = responses

    
    all_answered = all(response is not None for response in responses.values())

    
    col1, col2 = st.columns(2)
    with col1:
        if current_section > 0:
            if st.button('Previous Section'):
                st.session_state.section -= 1
                st.experimental_rerun()

    with col2:
        if current_section < total_sections - 1:
            if st.button('Next Section', disabled=not all_answered):
                st.session_state.section += 1
                st.experimental_rerun()
        else:
          if st.button('Submit', disabled=not all_answered):
            user_responses = {}
            for section_name, questions in st.session_state.responses.items():
                for question, response in questions.items():
                    user_responses[question] = response

            
            model_response = get_esg_evaluation_with_api(user_responses)

            # Display the model response in Streamlit
            st.write("Model Response:")
            st.write(model_response)

            # Save user responses along with the model response to a JSON file
            with open("user_responses_with_model.json", "w") as json_file:
                json.dump({"user_responses": user_responses, "model_response": model_response}, json_file, indent=4)
                   
if __name__ == '__main__':
    main()
