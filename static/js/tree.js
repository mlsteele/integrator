console.log('hello!')

$(function(){
  console.log('the document has loaded.')

  var $problem_input = $('input[name="problem-input"]')
  var $problem_solve_btn = $('input[name="problem-solve"]')
  var $problem_response = $('.problem-response')

  $problem_solve_btn.click(function(){
    var val = $problem_input.val()

    console.log("sending up problem ", val)
    $.ajax({
      url: '/API/solve',
      // data: {problem: encodeURIComponent("intx^2dx")},
      data: {problem: val},
      success: function(data) {
        console.log('It has returned!')
        console.log('data', data)

        $problem_response.empty()
        $problem_response.append(data)

        MathJax.Hub.Queue(["Typeset", MathJax.Hub, $problem_response[0]]);
      },
      error: function() {
        console.error('error from request!')
      }
    })
  })
})
