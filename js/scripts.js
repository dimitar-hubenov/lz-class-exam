class HamQSet {
    constructor(ham_class) {
        this.ham_class = ham_class;
        this.questions = [];
        this._current_question_idx = 0;
    }

    get ham_class() {
        return this._ham_class;
    }
    set ham_class(val) {
        if (val === 1 || val === 2) {
            this._ham_class = val;
        }
    }
    get exam_section() {
        return this._exam_section;
    }
    set exam_section(val) {
        if (val >= 1 && val <= 3) {
            this._exam_section = val;
        }
    }
    get questions() {
        return this._questions;
    }
    set questions(val) {
        this._questions = val;
    }

    get current_question_idx() {
        return this._current_question_idx;
    }
    set current_question_idx(val) {
        if (val >= 0 && val < this._questions.length) {
            this._current_question_idx = val;
        }
    }

    get_current_question() {
        return this.questions[this.current_question_idx];
    }

    static load_questions(ham_class, exam_section) {
        if (exam_section < 1 && exam_section > 3) {
            console.log("Invalid exam section requested!");
            return;
        }

        const xmlhttp = new XMLHttpRequest();
        let jsonObj = undefined;
        xmlhttp.onload = function () {
            jsonObj = JSON.parse(this.responseText);
        };
        xmlhttp.open("GET", "qbank/class" + ham_class + "-section" + exam_section + ".json", false);
        xmlhttp.send();

        return jsonObj;
    }

    static shuffle_questions(arr, n) {
        if (n > arr.length) {
            throw new RangeError("HamTest.shuffle_questions: more elements taken than available");
        }
        const shuffled = [...arr].sort(() => 0.5 - Math.random());
        return (shuffled.slice(0, n));
    }
}

class HamStudy extends HamQSet {
    constructor(ham_class, exam_section, shuffle) {
        super(ham_class);
        this.exam_section = exam_section;

        if (shuffle) {
            let _section_questions = HamTest.load_questions(ham_class, exam_section);
            this.questions = HamTest.shuffle_questions(_section_questions, _section_questions.length);
        } else {
            this.questions = HamTest.load_questions(ham_class, exam_section);
        }
    }
}

class HamTest extends HamQSet {
    constructor(ham_class) {
        super(ham_class);
        
        let _section_questions = [];
        for (let section_idx = 1; section_idx <= 3; section_idx++) {
            _section_questions = HamTest.load_questions(ham_class, section_idx);
            _section_questions = HamTest.shuffle_questions(_section_questions, 20);
            this.questions = this.questions.concat(_section_questions);
        }
        // let's mix all sections
        this.questions = HamTest.shuffle_questions(this.questions, this.questions.length);
    }

    store_answer(answered) {
        this.questions[this.current_question_idx].answered = answered;
    }

    get score() {
        let _score = 0;
        for (let idx = 0; idx <= this.current_question_idx; idx++) {
            if (this.questions[idx].answer === this.questions[idx].answered) {
                _score++;
            }
        }
        return _score;
    }
}
