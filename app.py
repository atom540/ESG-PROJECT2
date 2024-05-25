import streamlit as st
import json
from esg_evaluation import get_esg_evaluation_with_api 
from esg_evaluation import sasb_gri_report

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
        response = st.number_input(question, min_value=0, max_value=10, step=1, format="%d", key=key, value=response, on_change=update_response, args=(section_name, question, key))
        responses[question] = response
    st.session_state.responses[section_name] = responses  # Update session state with current responses
    return responses

def update_response(section_name, question, key):
    st.session_state.responses[section_name][question] = st.session_state[key]

if 'section' not in st.session_state:
    st.session_state.section = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {section: {} for section in sections}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'model_response' not in st.session_state:
    st.session_state.model_response = {}
if 'add_credentail_button' not in st.session_state:
    st.session_state.add_credentail_button = False
if 'add_credentail_submit' not in st.session_state:
    st.session_state.add_credentail_submit = False
if 'add_credentail_response' not in st.session_state:
    st.session_state.add_credentail_response = {
        "must_have": {},
        "good_to_have": {},
        "action_plan_and_score": {}
    }

def main():
    if st.session_state.add_credentail_submit:
        if 'add_credentail_response' in st.session_state:
            st.title("Model Response")
            
            # Access and print the response
            add_credentail_response = st.session_state.add_credentail_response
            st.write("Must-Have Practices:")
            st.write(add_credentail_response["must_have"])

            st.write("Good-To-Have Practices:")
            st.write(add_credentail_response["good_to_have"])

            st.write("Action Plan and Score:")
            st.write(add_credentail_response["action_plan_and_score"])

          

    elif st.session_state.submitted:
        if 'model_response' in st.session_state:
            st.title("Model Response")
            st.write(st.session_state.model_response)
            if st.button('Back to Form'):
                reset_form()
            if st.button('Add More Credential'):
                st.session_state.add_credentail_button=True
                

        if st.session_state.add_credentail_button :   
                #  add_more_credential()
                st.title("Add More Credential")
                industry_type = st.text_input("Industry Type", "")
                industry_size = st.text_input("Industry Size", "")
                industry_country = st.text_input("Industry Country", "")
                if st.button('Submit'):
                    # Load the previous user responses from the JSON file
                    with open("user_responses_with_model.json", "r") as json_file:
                        data = json.load(json_file)
                        user_responses = data["user_responses"]

                    # Generate model response based on the updated inputs
                    must_have, good_to_have, action_plan_and_score = sasb_gri_report(industry_type, industry_size, industry_country, user_responses)
                    
                    

                    st.session_state.add_credentail_response["must_have"] = must_have
                    st.session_state.add_credentail_response["good_to_have"] = good_to_have
                    st.session_state.add_credentail_response["action_plan_and_score"] = action_plan_and_score
                    st.session_state.add_credentail_submit = True
                    with open("add_credentail_response.json", "w") as json_file:
                        json.dump({"must_have":must_have ,"good_to_have":good_to_have,"action_plan_and_score":action_plan_and_score}, json_file)
                    
                    st.experimental_rerun()
                 
    else:
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
                    with st.spinner('Generating Model Response...'):
                        user_responses = {}
                        for section_name, questions in st.session_state.responses.items():
                            for question, response in questions.items():
                                user_responses[question] = response


                        with open("user_responses.json", "w") as json_file:
                            json.dump({"user_responses": user_responses}, json_file)

                        model_response = get_esg_evaluation_with_api(user_responses)
                    
                        with open("user_responses_with_model.json", "w") as json_file:
                            json.dump({"user_responses": user_responses, "model_response": model_response}, json_file)
                    # Store model response in session state
                    st.session_state.model_response = model_response
                    st.session_state.submitted = True

                    # Clear session state to avoid reruns
                    st.session_state.responses = {}

                    st.experimental_rerun()

def reset_form():
    st.session_state.submitted = False
    st.session_state.section = 0
    st.session_state.responses = {section: {} for section in sections}
    st.session_state.model_response = {}
    st.session_state.add_credentail_button=False
    st.experimental_rerun()


       

  

if __name__ == '__main__':
    main()
