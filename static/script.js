function getFormData() {
    return {
        name: document.getElementById("name").value,
        role: document.getElementById("role").value,
        skills: document.getElementById("skills").value,
        education: document.getElementById("education").value,
        projects: document.getElementById("projects").value,
        experience: document.getElementById("experience").value
    };
}

function generateResume() {
    fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(getFormData())
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("resumePreview").innerHTML = data.resume;
        document.getElementById("coverPreview").innerHTML = "<h2>Cover Letter</h2><p>" + data.cover_letter.replace(/\n/g, "<br>") + "</p>";
    });
}

function downloadPDF() {
    fetch("/download_pdf", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(getFormData())
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "Professional_Resume.pdf";
        a.click();
    });
}
function generatePortfolio() {
    const name = document.getElementById("p_name").value;
    const about = document.getElementById("p_about").value;
    const skills = document.getElementById("p_skills").value;
    const projects = document.getElementById("p_projects").value;

    const html = `
        <h1>${name}</h1>
        <h3>About Me</h3>
        <p>${about}</p>

        <h3>Skills</h3>
        <p>${skills}</p>

        <h3>Projects</h3>
        <p>${projects}</p>
    `;

    document.getElementById("portfolioPreview").innerHTML = html;
}
function analyzeResume() {
    const text = document.getElementById("analysisText").value;
    const length = text.length;

    let score = 0;

    if (length > 200) score += 30;
    if (text.includes("project")) score += 20;
    if (text.includes("experience")) score += 20;
    if (text.includes("%")) score += 20;
    if (length > 500) score += 10;

    document.getElementById("scoreResult").innerHTML =
        `<h3>Resume Score: ${score}/100</h3>`;

    const ctx = document.getElementById("analysisChart").getContext("2d");

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Content Length', 'Projects', 'Experience', 'Metrics', 'Depth'],
            datasets: [{
                label: 'Score Breakdown',
                data: [
                    length > 200 ? 30 : 10,
                    text.includes("project") ? 20 : 5,
                    text.includes("experience") ? 20 : 5,
                    text.includes("%") ? 20 : 5,
                    length > 500 ? 10 : 2
                ]
            }]
        }
    });
}
