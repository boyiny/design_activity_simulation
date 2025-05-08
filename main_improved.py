from openai import OpenAI
import os
from os.path import join, dirname
from dotenv import load_dotenv

from agent_individual_intelligence import DesignTeamAgents
from datetime import datetime
import csv


GATHER_USER_NEEDS_TURN_LIMIT = 3
GATHER_BUSINESS_ANALYSIS_TURN_LIMIT = 3
# GATHER_BUSINESS_ANALYSIS_WORD_LIMIT = 40
GATHER_ETHICAL_ADVICE_TURN_LIMIT = 3
GATHER_TECHNICAL_ANALYSIS_TURN_LIMIT = 3
GATHER_INTERACTION_DESIGN_TURN_LIMIT = 3

initial_question = {
    "BUSINESS_ANALYST": "Could you tell me your insights on the unique business insights, market size, market gaps, competitors, and business goals of the design task?",
    "ETHICS_ADVISOR": "Could you tell me your insights on the ethical implications, regulations, and constraints of the design task?",
    "DEVELOPER": "Could you tell me your insights on the technical feasibility, implimentation, and constraints of the design task?",
    "INTERACTION_DESIGNER": "Could you tell me your insights on the unique system features, user experience, and interaction design of the design task?",
}

evaluation_question = """Please provide a detailed summary that includes all ideas we just discussed, along with an evaluation of these ideas. \
    For the evaluation, you need to tell me the importance, the pros and cons, the feasibility, and the potential impact of these ideas on our topic. \
    Then you need to rank these ideas based on the overall evaluation. \
    Finally, you need to slecet a few ideas that you think are the most essential or promising and explain why you think so. """




class GroupIntelligence:
    def __init__(self, end_user_number) -> None:
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 
        self.model = "gpt-4o"
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        # self.client2 = OpenAI(api_key=OPENAI_API_KEY_2)
        self.thread_clarify_end_user = None
        self.thread_understand_user_needs = None
        self.thread_gather_business_analysis = None
        self.thread_pm = None # The main thread - Product Manager thread
        self.design_team_agents = None
        self.user_researcher_agent = None
        self.stakeholder_agent = []
        self.product_manager_agent = None
        self.business_analyst_agent = None
        self.ethics_advisor_agent = None
        self.developer_agent = None
        self.interation_designer_agent = None
        self.end_user_number = end_user_number


        # create files for each thread
        current_time = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"

        folder_name = f"data/{current_time}"
        os.makedirs(folder_name, exist_ok=True)

        # User persona
        self.file_name_history_clarify_end_user_persona = f"{folder_name}/history_clarify_end_user_persona.txt"
        with open(self.file_name_history_clarify_end_user_persona, 'w+') as file:
            pass
        
        # User needs
        self.file_name_history_gather_user_needs_list = []
        self.file_name_summary_gather_user_needs_list = []
        for i in range(self.end_user_number):
            self.file_name_history_gather_user_needs_list.append(f"{folder_name}/history_gather_user_needs_{i+1}.txt")
            with open(self.file_name_history_gather_user_needs_list[i], mode='w+') as file:
                pass
            self.file_name_summary_gather_user_needs_list.append(f"{folder_name}/summary_gather_user_needs_{i+1}.txt")
            with open(self.file_name_summary_gather_user_needs_list[i], mode='w+') as file:
                pass
        

        # Technical analysis
        self.file_name_history_gather_tech_analysis = f"{folder_name}/history_gather_tech_analysis.txt"
        with open(self.file_name_history_gather_tech_analysis, mode='w+') as file:
            pass
        self.file_name_summary_gather_tech_analysis = f"{folder_name}/summary_gather_tech_analysis.txt"
        with open(self.file_name_summary_gather_tech_analysis, mode='w+') as file:
            pass
        
        # Business analysis
        self.file_name_history_gather_business_analysis = f"{folder_name}/history_gather_business_analysis.txt"
        with open(self.file_name_history_gather_business_analysis, mode='w+') as file:
            pass
        self.file_name_summary_gather_business_analysis = f"{folder_name}/summary_gather_business_analysis.txt"
        with open(self.file_name_summary_gather_business_analysis, mode='w+') as file:
            pass

        # Ethical analysis
        self.file_name_history_gather_ethical_analysis = f"{folder_name}/history_gather_ethical_analysis.txt"
        with open(self.file_name_history_gather_ethical_analysis, mode='w+') as file:
            pass
        self.file_name_summary_gather_ethical_analysis = f"{folder_name}/summary_gather_ethical_analysis.txt"
        with open(self.file_name_summary_gather_ethical_analysis, mode='w+') as file:
            pass
        
        # Conceptual design
        self.file_name_history_gather_design_analysis = f"{folder_name}/history_gather_design_analysis.txt"
        with open(self.file_name_history_gather_design_analysis, mode='w+') as file:
            pass
        self.file_name_summary_gather_design_analysis = f"{folder_name}/summary_gather_design_analysis.txt"
        with open(self.file_name_summary_gather_design_analysis, mode='w+') as file:
            pass

        # Product Requirement Document
        self.file_name_prd = f"{folder_name}/product_requirement_document.txt"
        with open(self.file_name_prd, mode='w+') as file:
            pass

        
        # Individual Intelligence: Create agents and define their properties
        # 
        # Group Intelligence: Define the code of conduct for the agents in the group
        # 
        # Collective Intelligence: Observe how user agents interact with the conceptual design


        # Group Intelligence: Define the code of conduct for the agents in the group
        # Step 1: Human input a rough design task
        # Step 2: User researcher receives the task and indicates the target users. 
        # Step 3: User researcher probe the stakeholders and gather user needs, using user research techniques. Make a summary of the user needs and context information. 
        # Step 4: Product manager access the summary of the user researcher. Product manager understands the user needs and context information. 
        # Step 5.1: Having this information, the product manager asks the business analyst to provide a business analysis of the design task. Product manager understands the business goals and constraints.
        # Step 5.2: Having this information, the product manager asks the ethics advisor to provide an ethical analysis of the design task. Product manager understands the ethical implications and constraints.
        # Step 5.3: Having this information, the product manager asks the developer to provide a technical analysis of the design task. Product manager understands the technical feasibility and constraints.
        # Step 6: Product manager summarizes the user needs, technical feasibility, business goals, and ethical implications. Product manager provides a conceptual design of the product, describing the features of the product.
        # Step 7: Interaction designer receives the conceptual design and creates a detailed design of the product, describing the user interface and user experience.


    # === Step 1: Human input a rough design task ===
    def createDesignTask(self):
        # Human input a rough design task

        # design_task = "Design an app that helps overweight people form a healthy lifestyle."
        design_task = input("Please input a design task: ") # Design a human-in-the-loop system driven by multiple AI agents for product innovation. 
        # design_task = "Desin a virtual career coach system that plays MBA career office role to help MBA students navigate career deevlopment with structure and efficiency."
        # design_task = "Design an app that helps students take online couses."
        return design_task
    
    # === Step 2: User researcher receives the task and indicates the target users. ===
    def clarifyStakeholderIdentity(self, end_user_number, design_task):
        # Stakeholder receives the task and clarify their identity
        if end_user_number == 1:
            word_persona = "persona"
        else:
            word_persona = "personas"

        thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    This is the <DESIGN_TASK>: {design_task}. Please indicate {end_user_number} unique user {word_persona} that strongly correlated to this design task, with detailed demographic information, typical traits, personalities, and figures, previous experience and essential personal information that are relevant to the task. \
                    Each persona should be a representive of a unique user group who may have same and/or different needs, motivations, status, barriers, etc. \
                    The user group may not be categorized by end users' occupations, it can be categorized by their needs, motivations, status, barriers, etc. \
                    However, never propose any system features. \
                    You must only answer the persona with pure text format. No extra words. Each persona should be separated by '====='.
                    """
                }
            ]
        )
        self.thread_clarify_end_user = thread
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_clarify_end_user.id,
            assistant_id=self.user_researcher_agent.id,
            instructions="Please clarify the persona." 
        )

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            print(f"User persona: {messages.data[0].content[0].text.value}")
            self.log_conversation("User persona", messages.data[0].content[0].text.value, self.file_name_history_clarify_end_user_persona)
            persona_all = messages.data[0].content[0].text.value
            persona_list = persona_all.split("=====")
            persona_list = [persona.strip() for persona in persona_list]
            persona_list = [persona.strip() for persona in persona_list if len(persona) > 10] # Remove empty or low quality persona
            persona_list = persona_list[:end_user_number] # Limit the number of persona
            print("Persona List:")
            print(persona_list)


            return persona_list
        else:
            print(f"User identity run status: {run.status}")
        
    # === Step 3: User researcher probe the stakeholders and gather user needs. ===
    def gatherUserNeeds(self, stakeholder_agent, chat_turn_limit, user_index):
        thread = self.client.beta.threads.create()
        self.thread_understand_user_needs = thread

        n = 0
        # User Researcher ask the first question to the stakeholder
        # self.log_summary(f"=======USER {user_index+1}=======\n", self.file_name_history_gather_user_needs_list[user_index]) # Add user index to the conversation
        user_researcher_msg = "Could you tell me a little about yourself?" 
        self.log_conversation("User Researcher", user_researcher_msg, self.file_name_history_gather_user_needs_list[user_index])
        print(f"\n\nUser researcher: \n{user_researcher_msg}\n")

        # Stakeholder answers the first question from the user researcher
        user_researcher_message = self.client.beta.threads.messages.create(
            thread_id=self.thread_understand_user_needs.id,
            role="user",
            content=user_researcher_msg
        )

        run_stakeholder_answer = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_understand_user_needs.id,
            assistant_id=stakeholder_agent.id,
            additional_instructions="Please keep giving me detailed and insightful answers."
        )
        if run_stakeholder_answer.status == "completed":
                stakeholder_message = self.client.beta.threads.messages.list(thread_id=self.thread_understand_user_needs.id)
                stakeholder_msg = stakeholder_message.data[0].content[0].text.value
                self.log_conversation("User", stakeholder_msg, self.file_name_history_gather_user_needs_list[user_index])
                print(f"\nUser: \n{stakeholder_msg}\n") 
        else:
            print(f"In gatherUserNeeds, run_stakeholder_answer status: {run_stakeholder_answer.status}")

        while n < chat_turn_limit:
            n += 1

            # User Researcher ask questions to the stakeholder 
            run_user_researcher_ask = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread_understand_user_needs.id,
                assistant_id=self.user_researcher_agent.id,
                additional_instructions=stakeholder_msg # Regulate the format of the message if necessary
            )
            if run_user_researcher_ask.status == "completed":
                user_researcher_message = self.client.beta.threads.messages.list(thread_id=self.thread_understand_user_needs.id)
                user_researcher_msg = user_researcher_message.data[0].content[0].text.value
                self.log_conversation("User Researcher", user_researcher_msg, self.file_name_history_gather_user_needs_list[user_index])
                print(f"\nUser Researcher: \n{user_researcher_msg}\n")
            else:
                print(f"In gatherUserNeeds, run_user_researcher_ask status: {run_user_researcher_ask.status}")

            # Stakeholder answers the questions from the user researcher
            run_stakeholder_answer = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread_understand_user_needs.id,
                assistant_id=stakeholder_agent.id,
                additional_instructions=user_researcher_msg
            )
            if run_stakeholder_answer.status == "completed":
                stakeholder_message = self.client.beta.threads.messages.list(thread_id=self.thread_understand_user_needs.id)
                stakeholder_msg = stakeholder_message.data[0].content[0].text.value
                self.log_conversation("User", stakeholder_msg, self.file_name_history_gather_user_needs_list[user_index])
                print(f"\nUser: \n{stakeholder_msg}\n")
            else:
                print(f"In gatherUserNeeds, run_stakeholder_answer status: {run_stakeholder_answer.status}")
        
            print(f"\nGather User Needs Turn: {n}\n")
        
    def createPRD(self, pm_agent, design_task, file_name_user_study_summary=None, file_name_business_analysis_summary=None, file_name_technical_analysis_summary=None, file_name_ethical_analysis_summary=None, file_name_design_analysis_summary=None):
        thread_pm = self.client.beta.threads.create()
        pm_agent = self.design_team_agents.updateProductManagerFor("Client", pm_agent, design_task, file_name_user_study_summary, file_name_business_analysis_summary, file_name_technical_analysis_summary, file_name_ethical_analysis_summary, file_name_design_analysis_summary)
        self.product_manager_agent = pm_agent

        # Agent answers the detail of the analysis
        run_agent_answer = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_pm.id,
            assistant_id=pm_agent.id,
            additional_instructions="Please create a detailed and executable Product Requirement Document (PRD) based on the provided information."
        )
        if run_agent_answer.status == "completed":
                agent_message = self.client.beta.threads.messages.list(thread_id=thread_pm.id)
                agent_msg = agent_message.data[0].content[0].text.value
                self.log_conversation(pm_agent.name, agent_msg, self.file_name_prd)
                print(f"\n{pm_agent.name}: \n{agent_msg}\n")
        else:
            print(f"In gatherAnalysisFrom, run_agent_answer status: {run_agent_answer.status}")




    # === Shared Functions ===
    def log_summary(self, summary, file_name):
        with open(file_name, mode='a') as file:
            file.write(summary)

    def log_conversation(self, role, message, file_name):
        with open(file_name, mode='a') as file:
            file.write(f"### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n## >>> {role}: \n{message}\n\n\n")

    def getSummaryFromProductManager(self, summary_prompt, input_file_name, output_file_name):
        user_study_summary = None
        # load the file to the thread
        file = self.client.files.create(
            file=open(input_file_name, "rb"),
            purpose="assistants"
        )

        
        thread = self.client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": summary_prompt, 
                "attachments": [{
                    "file_id": file.id,
                    "tools": [{"type": "code_interpreter"}]
                }]
                
            }]
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=self.product_manager_agent.id,
            # instructions="Please only provide a detailed summary of the user study. Do not add anything else."
        )

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            user_study_summary = messages.data[0].content[0].text.value
            print(f"Productor Manager - Conversation Summary: {user_study_summary}")
        else:
            print(f"Product Manager - Conversation summary run status: {run.status}")

        self.log_summary(user_study_summary, output_file_name)

        return user_study_summary

    def gatherAnalysisFrom(self, agent, pm_agent, design_task, initial_question, chat_turn_limit, file_name_history_to_be_saved):
        thread_pm = self.client.beta.threads.create()

        print(f"Agent: {agent.name}")
        pm_agent = self.design_team_agents.updateProductManagerFor(agent.name, pm_agent, design_task)
        self.product_manager_agent = pm_agent

        n = 0

        # Product manager asks the agent to provide an analysis of the design task
        product_manager_msg = initial_question
        self.log_conversation("Product Manager", product_manager_msg, file_name_history_to_be_saved)
        print(f"\n\nProduct Manager: \n{product_manager_msg}\n")

        product_manager_message = self.client.beta.threads.messages.create(
            thread_id=thread_pm.id,
            role="user",
            content=product_manager_msg
        )

        # Agent answers the detail of the analysis
        run_agent_answer = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_pm.id,
            assistant_id=agent.id,
            additional_instructions="Please keep giving me detailed and insightful answers."
        )
        if run_agent_answer.status == "completed":
                agent_message = self.client.beta.threads.messages.list(thread_id=thread_pm.id)
                agent_msg = agent_message.data[0].content[0].text.value
                self.log_conversation(agent.name, agent_msg, file_name_history_to_be_saved)
                print(f"\n{agent.name}: \n{agent_msg}\n")
        else:
            print(f"In gatherAnalysisFrom, run_agent_answer status: {run_agent_answer.status}")
        

        while n < chat_turn_limit:
            n += 1

            # Product Manager ask questions to the agent
            run_product_manager_ask = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_pm.id,
                assistant_id=pm_agent.id,
                additional_instructions=agent_msg
            )
            if run_product_manager_ask.status == "completed":
                product_manager_message = self.client.beta.threads.messages.list(thread_id=thread_pm.id)
                product_manager_msg = product_manager_message.data[0].content[0].text.value
                self.log_conversation("Product Manager", product_manager_msg, file_name_history_to_be_saved)
                print(f"\nProduct Manager: \n{product_manager_msg}\n")
            else:
                print(f"In gatherAnalysisFrom, run_product_manager_ask status: {run_product_manager_ask.status}")

            # Agent answers the questions from the Product Manager
            run_agent_answer = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_pm.id,
                assistant_id=agent.id,
                additional_instructions=product_manager_msg
            )
            if run_agent_answer.status == "completed":
                agent_message = self.client.beta.threads.messages.list(thread_id=thread_pm.id)
                agent_msg = agent_message.data[0].content[0].text.value
                self.log_conversation(agent.name, agent_msg, file_name_history_to_be_saved)
                print(f"\n{agent.name}: \n{agent_msg}\n")
            else:
                print(f"In gatherAnalysisFrom, run_{agent.name}_answer status: {run_agent_answer.status}")

            print(f"\nGather {agent.name} Analysis Turn: {n}\n")

        # === The additional turn for evaluating ideas. === 
        
        # Product manager asks the agent to provide a detailed summarize along with an evaluation of the ideas.
        product_manager_msg = evaluation_question
        self.log_conversation("Product Manager", product_manager_msg, file_name_history_to_be_saved)
        print(f"\n\nProduct Manager: \n{product_manager_msg}\n")

        product_manager_message = self.client.beta.threads.messages.create(
            thread_id=thread_pm.id,
            role="user",
            content=product_manager_msg
        )

        # Agent answers the detail of the analysis
        run_agent_answer = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_pm.id,
            assistant_id=agent.id,
            additional_instructions="Please keep giving me detailed and insightful answers."
        )
        if run_agent_answer.status == "completed":
                agent_message = self.client.beta.threads.messages.list(thread_id=thread_pm.id)
                agent_msg = agent_message.data[0].content[0].text.value
                self.log_conversation(agent.name, agent_msg, file_name_history_to_be_saved)
                print(f"\n{agent.name}: \n{agent_msg}\n")
        else:
            print(f"In gatherAnalysisFrom, run_agent_answer status: {run_agent_answer.status}")
        



                
    def run(self, end_user_number):
        self.design_team_agents = DesignTeamAgents(client=self.client, model=self.model)
        DESIGN_EVENT = ""
        
        # Step 1: Human input a rough design task
        design_task = self.createDesignTask()
        print(f"Design Task: {design_task}")
        
        # Step 2: User researchers receives the task and indicates the target users. 
        # Create user researcher agent
        self.user_researcher_agent = self.design_team_agents.createUserResearcherAgent(design_task)
        end_user_persona_list = self.clarifyStakeholderIdentity(end_user_number, design_task)

        # self.file_name_history_gather_user_needs_list = ["data/20240822113951/history_gather_user_needs_1.txt", "data/20240822113951/history_gather_user_needs_2.txt", "data/20240822113951/history_gather_user_needs_3.txt", "data/20240822113951/history_gather_user_needs_4.txt", "data/20240822113951/history_gather_user_needs_5.txt", "data/20240822113951/history_gather_user_needs_6.txt", "data/20240822113951/history_gather_user_needs_7.txt", "data/20240822113951/history_gather_user_needs_8.txt"]
        
        for i, end_user_persona in enumerate(end_user_persona_list):
            # Clarify the stakeholder identity
            print(f"\n === End User Persona {i+1} === \n")
            print(end_user_persona)
            # Clarify the stakeholder identity
            
            # Create stakeholder agent
            stakeholder_agent = self.design_team_agents.createStakeholderAgent(design_task, end_user_persona)
            self.stakeholder_agent.append(stakeholder_agent)

            # Step 3: User researcher probe the stakeholders and gather user needs. Make a summary of the user needs and context information.
            DESIGN_EVENT = "GAHTER_USER_NEEDS"
            self.gatherUserNeeds(stakeholder_agent, GATHER_USER_NEEDS_TURN_LIMIT, i)


            # Step 4: Product manager access the summary of the user researcher. Product manager understands the user needs and context information.
            self.product_manager_agent = self.design_team_agents.createProductManagerAgent(design_task)
            summary_prompt = self.design_team_agents.getSummaryPrompt(design_task, DESIGN_EVENT)
            user_study_summary = self.getSummaryFromProductManager(summary_prompt, self.file_name_history_gather_user_needs_list[i], self.file_name_summary_gather_user_needs_list[i]) # 
            # user_study_summary = self.getSummaryFromProductManager(design_task, "data/20240822113951/history_gather_user_needs.txt", self.file_name_summary_gather_user_needs_list[i]) # 
        
        # # Test the user study summary
        # self.product_manager_agent = self.design_team_agents.createProductManagerAgent(design_task)
        # self.file_name_summary_gather_user_needs_list = []
        # folder_name = "data/design_activity_eight_users"
        # for i in range(self.end_user_number):
        #     self.file_name_summary_gather_user_needs_list.append(f"{folder_name}/summary_gather_user_needs_{i+1}.txt")


        # # Step 5.1: Having this information, the product manager asks the business analyst to provide a business analysis of the design task. Product manager understands the business goals and constraints.
        DESIGN_EVENT = "GAHTER_BUSINESS_ANALYSIS"
        # Create business analyst agent
        self.business_analyst_agent = self.design_team_agents.createBusinessAnalystAgent(design_task, self.file_name_summary_gather_user_needs_list, self.file_name_summary_gather_business_analysis, self.file_name_summary_gather_tech_analysis, self.file_name_summary_gather_ethical_analysis, self.file_name_summary_gather_design_analysis)        
        self.gatherAnalysisFrom(self.business_analyst_agent, self.product_manager_agent, design_task, initial_question["BUSINESS_ANALYST"], GATHER_BUSINESS_ANALYSIS_TURN_LIMIT, self.file_name_history_gather_business_analysis)
        # Summary
        summary_prompt = self.design_team_agents.getSummaryPrompt(design_task, DESIGN_EVENT)
        business_analysis_summary = self.getSummaryFromProductManager(summary_prompt, self.file_name_history_gather_business_analysis, self.file_name_summary_gather_business_analysis)
        # self.file_name_business_analysis_summary = "data/design_activity_eight_users/summary_gather_business_analysis.txt"
        
        # Step 5.2: Having this information, the product manager asks the ethics advisor to provide an ethical analysis of the design task. Product manager understands the ethical implications and constraints.
        DESIGN_EVENT = "GAHTER_ETHICAL_ANALYSIS"
        # Create ethics advisor agent
        self.ethics_advisor_agent = self.design_team_agents.createEthicsAdvisorAgent(design_task, self.file_name_summary_gather_user_needs_list, self.file_name_summary_gather_business_analysis, self.file_name_summary_gather_tech_analysis, self.file_name_summary_gather_ethical_analysis, self.file_name_summary_gather_design_analysis)
        # Analyze
        self.gatherAnalysisFrom(self.ethics_advisor_agent, self.product_manager_agent, design_task, initial_question["ETHICS_ADVISOR"], GATHER_ETHICAL_ADVICE_TURN_LIMIT, self.file_name_history_gather_ethical_analysis)
        # Summary
        summary_prompt = self.design_team_agents.getSummaryPrompt(design_task, DESIGN_EVENT)
        ethical_analysis_summary = self.getSummaryFromProductManager(summary_prompt, self.file_name_history_gather_ethical_analysis, self.file_name_summary_gather_ethical_analysis)
        # self.file_name_ethical_analysis_summary = "data/design_activity_eight_users/summary_gather_ethical_analysis.txt"
        
        # Setp 5.4: Having this information, the product manager asks the interaction designer to provide a detailed design of the product, describing the user interface and user experience. 
        DESIGN_EVENT = "GAHTER_DESIGN_ANALYSIS"
        # Create interaction designer agent
        self.interation_designer_agent = self.design_team_agents.createInteractionDesignerAgent(design_task, self.file_name_summary_gather_user_needs_list, self.file_name_summary_gather_business_analysis, self.file_name_summary_gather_tech_analysis, self.file_name_summary_gather_ethical_analysis, self.file_name_summary_gather_design_analysis)
        # Analyze
        self.gatherAnalysisFrom(self.interation_designer_agent, self.product_manager_agent, design_task, initial_question["INTERACTION_DESIGNER"], GATHER_INTERACTION_DESIGN_TURN_LIMIT, self.file_name_history_gather_design_analysis)
        # Summary
        summary_prompt = self.design_team_agents.getSummaryPrompt(design_task, DESIGN_EVENT)
        interaction_design_summary = self.getSummaryFromProductManager(summary_prompt, self.file_name_history_gather_design_analysis, self.file_name_summary_gather_design_analysis)
        # self.file_name_interaction_design_summary = "data/data_design_activity_eight_users/summary_gather_conceptual_design.txt"


        # Step 5.3: Having this information, the product manager asks the developer to provide a technical analysis of the design task. Product manager understands the technical feasibility and constraints.
        DESIGN_EVENT = "GAHTER_TECHNICAL_ANALYSIS"
        # Create developer agent
        # file_name_tech_analysis_summary = ""
        
        self.developer_agent = self.design_team_agents.createDeveloperAgent(design_task, self.file_name_summary_gather_user_needs_list, self.file_name_summary_gather_business_analysis, self.file_name_summary_gather_tech_analysis, self.file_name_summary_gather_ethical_analysis, self.file_name_summary_gather_design_analysis)
        # # Analyze
        self.gatherAnalysisFrom(self.developer_agent, self.product_manager_agent, design_task, initial_question["DEVELOPER"], GATHER_TECHNICAL_ANALYSIS_TURN_LIMIT, self.file_name_history_gather_tech_analysis)
        # # Summary
        summary_prompt = self.design_team_agents.getSummaryPrompt(design_task, DESIGN_EVENT)
        technical_analysis_summary = self.getSummaryFromProductManager(summary_prompt, self.file_name_history_gather_tech_analysis, self.file_name_summary_gather_tech_analysis)
        # file_name_tech_analysis_summary = "data/data_design_activity_eight_users/summary_gather_tech_analysis.txt"
        
       
        
        # Step 6: Product manager create a product requirement document (PRD) based on all the analyses results from these agents
        # Update the product manager agent

        # Create a PRD
        self.createPRD(self.product_manager_agent, design_task, self.file_name_summary_gather_user_needs_list, self.file_name_summary_gather_business_analysis, self.file_name_summary_gather_tech_analysis, self.file_name_summary_gather_ethical_analysis, self.file_name_summary_gather_design_analysis)




if __name__ == "__main__":
    end_user_number = 8
    group_intelligence = GroupIntelligence(end_user_number)
    group_intelligence.run(end_user_number)