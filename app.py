from flask import Flask, render_template, request

app = Flask(__name__)

def max_grade(labs, assignments, mid_exam, final_exam, bonus):
    for index in range(len(labs), 13):
        labs.insert(index, 100)
    for index in range(len(assignments), 7):
        assignments.insert(index, 100)

    lab_avg = (sum(labs) - min(labs)) / 12
    assignment_avg = (sum(assignments) - min(assignments)) / 6

    lab_worth = lab_avg * 0.10
    assignment_worth = assignment_avg * 0.40
    final_exam += bonus
    if final_exam > mid_exam:
        mid_exam = final_exam

    mid_worth = mid_exam * 0.20
    final_worth = final_exam * 0.30
    overall_score = lab_worth + assignment_worth + mid_worth + final_worth

    if overall_score >= 89.5:
        grade = "A"
    elif overall_score >= 79.5:
        grade = "B"
    elif overall_score >= 69.5:
        grade = "C"
    elif overall_score >= 59.5:
        grade = "D"
    else:
        grade = "F"
    return overall_score, grade, lab_avg, assignment_avg


def min_grade(labs, assignments, mid_exam, final_exam, bonus):
    for index in range(len(labs), 13):
        labs.insert(index, 0)
    for index in range(len(assignments), 7):
        assignments.insert(index, 0)

    lab_avg = (sum(labs) - min(labs)) / 12
    assignment_avg = (sum(assignments) - min(assignments)) / 6

    lab_worth = lab_avg * 0.10
    assignment_worth = assignment_avg * 0.40
    final_exam += bonus
    if final_exam > mid_exam:
        mid_exam = final_exam

    mid_worth = mid_exam * 0.20
    final_worth = final_exam * 0.30
    overall_score = lab_worth + assignment_worth + mid_worth + final_worth

    if overall_score >= 89.5:
        grade = "A"
    elif overall_score >= 79.5:
        grade = "B"
    elif overall_score >= 69.5:
        grade = "C"
    elif overall_score >= 59.5:
        grade = "D"
    else:
        grade = "F"
    return overall_score, grade, lab_avg, assignment_avg


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    labs = [""] * 13
    assignments = [""] * 7
    mid_exam = final_exam = bonus = ""

    if request.method == "POST":
        try:
            labs = [x.strip() for x in request.form.getlist("labs")]
            assignments = [x.strip() for x in request.form.getlist("assignments")]
            mid_exam = float(request.form.get("mid", 0) or 0)
            final_exam = float(request.form.get("final", 0) or 0)
            bonus = float(request.form.get("bonus", 0) or 0)

            # Convert filled values to floats
            labs_filled = [float(x) for x in labs if x != ""]
            assignments_filled = [float(x) for x in assignments if x != ""]

            # Check if any box is empty
            has_missing = (len(labs_filled) < 13) or (len(assignments_filled) < 7)

            if has_missing:
                # Min grade assumes 0 for empty, max grade assumes 100 for empty
                labs_min = [float(x) if x != "" else 0 for x in labs]
                assignments_min = [float(x) if x != "" else 0 for x in assignments]
                labs_max = [float(x) if x != "" else 100 for x in labs]
                assignments_max = [float(x) if x != "" else 100 for x in assignments]

                min_score, min_g, lab_min, asg_min = min_grade(labs_min, assignments_min, mid_exam, final_exam, bonus)
                max_score, max_g, lab_max, asg_max = max_grade(labs_max, assignments_max, mid_exam, final_exam, bonus)

                result = {
                    "type": "range",
                    "min_g": min_g,
                    "max_g": max_g,
                    "min_score": min_score,
                    "max_score": max_score,
                    "lab_min": lab_min,
                    "lab_max": lab_max,
                    "asg_min": asg_min,
                    "asg_max": asg_max,
                }
            else:
                labs = [float(x) for x in labs]
                assignments = [float(x) for x in assignments]
                score, grade, lab_avg, asg_avg = max_grade(labs, assignments, mid_exam, final_exam, bonus)
                result = {
                    "type": "exact",
                    "grade": grade,
                    "score": score,
                    "lab_avg": lab_avg,
                    "asg_avg": asg_avg,
                }

        except ValueError:
            result = {"error": "Please enter valid numeric values."}

    return render_template(
        "index.html",
        result=result,
        labs=labs,
        assignments=assignments,
        mid_exam=mid_exam,
        final_exam=final_exam,
        bonus=bonus,
    )


if __name__ == "__main__":
    app.run(debug=True)
