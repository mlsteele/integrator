$(function(){
  console.log('script loaded.')

  var $problem_input = $('input[name="problem-input"]')
  var $problem_solve_btn = $('input[name="problem-solve"]')
  var $problem_status = $('.problem-status')
  var $problem_response = $('.problem-response')

  function show_status(status) {
    // status can be "solved", "fetching", or "error"
    if (status != "fetching") {
      $problem_status.text(status)
      $problem_input.removeClass()
      $problem_input.addClass("status-" + status)
    }
  }

  function fetch_problem_solution() {
    var val = $problem_input.val()
    show_status("fetching")

    console.log("sending problem to server ", val)
    $.ajax({
      url: '/API/solve',
      // data: {problem: encodeURIComponent("intx^2dx")},
      data: {problem: val},
      success: function(data) {
        console.log('solution received from server.')
        // console.log('data', data)

        show_status("solved")
        $problem_response.empty()
        $problem_response.append(data)

        MathJax.Hub.Queue(["Typeset", MathJax.Hub, $problem_response[0]]);
      },
      error: function() {
        console.error('error from request!')
        show_status("error")
      }
    })
  }

  $problem_solve_btn.click(fetch_problem_solution)
  $problem_input.keyup(fetch_problem_solution)

  $problem_solve_btn.click();
})
