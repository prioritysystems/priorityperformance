const motivationModal = () => {
    Swal.fire({
        text: 'What is it about the person you are nominating that has motivated you to nominate them as an African Genius?',
    })
    sessionStorage.setItem('motivationModal', 'clicked')
}


const skillCategory = () => {

    Swal.fire({
        text: 'What skills does the individual have that motivated you to nominate them as an African Genius?',
    })

    sessionStorage.setItem('skillCategory', 'clicked')

}


const skillRecognition = () => {

    Swal.fire({
        text: 'Please state why it is an easy or not easy skill to recognize/appreciate based on its impact or necessity in your society.',
    })

    sessionStorage.setItem('skillRecognition', 'clicked')

}


const skillRarityScale = () => {

    Swal.fire({
        text: 'How rare are the above-mentioned skills on a scale of 0 to 100, 0 is not rare and 100 is extremely rare',
    })

    sessionStorage.setItem('skillRarityScale', 'clicked')

}

const skillRarity = () => {

    Swal.fire({
        text: 'Please give a reason for your rating in the previous question.',
    })

    sessionStorage.setItem('skillRarity', 'clicked')

}


const skillUsage = () => {

    Swal.fire({
        text: 'List/mention some of the problems that are being addressed within our society by the individual using the skill you mentioned above.',
    })

    sessionStorage.setItem('skillUsage', 'clicked')

}



const skillApplication = () => {

    Swal.fire({
        text: 'What has the individual done to solve the important problems you listed above?',
    })

    sessionStorage.setItem('skillApplication', 'clicked')

}



const awardDetails = () => {
    Swal.fire({
        text: 'Please don’t forget to mention the name of the award, where it is from and the year.',
    })

    sessionStorage.setItem('awardDetails', 'clicked')

}


document.querySelector('#id_sec_b_q1').addEventListener('click', () => {
    if (sessionStorage.getItem('motivationModal') != 'clicked') { motivationModal() }
})


document.querySelector("#id_sec_b_q1_1").addEventListener('click', () => {
    if (sessionStorage.getItem('skillCategory') != 'clicked') { skillCategory() }
})


document.querySelector("#id_sec_b_q1_2").addEventListener('click', () => {

    if (sessionStorage.getItem('skillRecognition') != 'clicked') { skillRecognition() }

})



document.querySelector("#id_sec_b_q3").addEventListener('click', () => {

    if (sessionStorage.getItem('skillRarityScale') != 'clicked') { skillRarityScale() }

})


document.querySelector("#id_sec_b_q3_1").addEventListener('click', () => {

    if (sessionStorage.getItem('skillRarity') != 'clicked') { skillRarity() }

})


document.querySelector("#id_sec_b_q5").addEventListener('click', () => {

    if (sessionStorage.getItem('skillUsage') != 'clicked') { skillUsage() }

})


document.querySelector("#id_sec_b_q5_2").addEventListener('click', () => {

    if (sessionStorage.getItem('skillApplication') != 'clicked') { skillApplication() }

})


document.querySelector("#id_sec_b_q7").addEventListener('click', () => {

    if (sessionStorage.getItem('awardDetails') != 'clicked') { awardDetails() }

})