## study session in daily activity choices
label study_session:
    hide screen player_stats_screen
    scene bg laptop_screen with dissolve

    # correct choices increments CS knowledge
    $ timeout_label = None # no time limit
    $ num_questions = 4 # ask 4 questions each time
    $ num_correct = 0
    while num_questions > 0:
        if num_questions == 4:
            player neutral "First question."
        elif num_questions == 3:
            player neutral "Second question. Halfway through!"
        elif num_questions == 2:
            player neutral "Third question. Almost there!"
        elif num_questions == 1:
            player neutral "Last question. Hang in there!"

        $ num_questions -= 1

        window hide
        # see cs_questions.rpy
        $ quiz_question = renpy.random.choice(study_session_questions)
        if quiz_question.code_label is not None:
            show screen example(quiz_question.code_label)

        # display question
        $ renpy.say(None, quiz_question.question, interact=False)
        # result is True or False
        $ result = renpy.display_menu(quiz_question.choices)
        hide screen example

        if result == True:
            $ num_correct += 1
            $ player_stats.change_stats('CS Knowledge', 5)
            player happy "Correct!"
        else:
            with vpunch
            player pout "Wrong..."
            # show the correct answer and explanation using a viewport
            call screen quiz_question_answer_explanation_screen(quiz_question)

        # hide player stats screen if it was showing so it doesn't obstruct the questions
        hide screen player_stats_screen

    play sound 'audio/sfx/quiz_complete.wav'
    pause 0.5
    player neutral "All done!"

    return

## hacker space trivia session
label trivia_session:
    $ num_questions = len(trivia_questions)
    $ num_correct = 0

    $ timeout_label = 'trivia_session_questions'
    $ timeout = 30.0 # 30 seconds for each question

    # fall through to the next label

label trivia_session_questions:
    while num_questions > 0:
        if num_questions == len(trivia_questions):
            trivia_guy "Here's the first question."
        elif num_questions == 1:
            trivia_guy "Last question."
        else:
            trivia_guy "Next question."
        call trivia_one_question from _call_trivia_one_question

    # check results
    trivia_guy "Now let's check the results."
    play sound 'audio/sfx/hacker_space_trivia_evaluate.wav'
    trivia_guy "...{w=0.5}...{w=0.5}...{w=0.5}"
    if num_correct == len(trivia_questions):
        trivia_guy "Could this be...?"
        play sound 'audio/sfx/hacker_space_trivia_win.wav'
        trivia_guy "You are the first person to get everything correct! Congratulations!"
        trivia_guy "Now about the award..."
        show business_card at truecenter with zoomin
        trivia_guy "I'm actually a talent recruiter at {b}CupcakeCPU™{/b}. Feel free to apply to our roles. We welcome talent like you."
        hide business_card
        trivia_guy "Until next time!"
        hide man with dissolve
        player "Uhhh... cool? I guess?"
        player "Let's add it to my To-Do list to apply to their company once I'm comfortable with my skill level."
        $ todo_list.add_todo(todo_apply_cupcakecpu)
        $ has_won_hacker_space_trivia = True

    else:
        trivia_guy "You missed some of the questions there, but it was close."
        trivia_guy "Better luck next time. I'll be here waiting."

    # remove the timed menu
    $ timeout_label = None
    $ timeout = None

    return

label trivia_one_question:
    $ num_questions -= 1
    $ quiz_question = trivia_questions[num_questions]
    if quiz_question.code_label is not None:
        show screen example(quiz_question.code_label)

    # display question
    $ renpy.say(None, quiz_question.question, interact=False)
    # result is True or False
    $ result = renpy.display_menu(quiz_question.choices)

    if result == True:
        $ num_correct += 1
        trivia_guy "That's right!"
    else:
        with vpunch
        trivia_guy "Nope."
        trivia_guy "The correct answer was {b}[quiz_question.true]{/b}"

    return

## coding interview session
label interview_session:
    $ num_questions = 5
    $ num_correct = 0

    $ timeout_label = 'interview_session_questions'
    $ timeout = 180.0 # three minutes for each question

    # fall through to the next label

label interview_session_questions:
    while num_questions > 0:
        if num_questions == 5:
            interviewer "Here's the first question."
        elif num_questions == 1:
            interviewer "Last question."
        else:
            interviewer "Next question."
        call interview_one_question from _call_interview_one_question

    # reset timeout
    $ timeout = None
    $ timeout_label = None

    # check results
    if num_correct == num_questions:
        $ offer_company_name = interview_company_name
    elif num_correct >= num_questions * 0.8:
        if renpy.random.random() < 0.6: # 60% chance of offer
            $ offer_company_name = interview_company_name

    return

label interview_one_question:
    $ num_questions -= 1
    # choose randomly from all available questions
    $ quiz_question = renpy.random.choice(interview_questions)
    if quiz_question.code_label is not None:
        show screen example(quiz_question.code_label)

    # display question
    $ renpy.say(None, quiz_question.question, interact=False)
    # result is True or False
    $ result = renpy.display_menu(quiz_question.choices)
    hide screen example

    if result == True:
        $ num_correct += 1

    return