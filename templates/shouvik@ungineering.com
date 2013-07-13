{% extends 'client-dashboard.html' %}


 {% block navlist %}
                        <ul class="nav nav-list">
                            <li>
                                <a href="/client-dashboard/client-tests" style="background-image: none; background-position: 0% 0%; background-repeat: repeat repeat;">Your tests</a>
                            </li>
                            <li class="active">
                                <a href="/client-dashboard/upload-test" style="background-image: none; background-position: 0% 0%; background-repeat: repeat repeat;">Upload a test</a>
                            </li>
                            <li></li>
                        </ul>
                     {% endblock %}




{% block content %}

<body>
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.3/jquery.min.js"> </script> 
    <script type="text/javascript" src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/js/bootstrap.min.js"> </script>
    <script type="text/javascript" src="http://tarruda.github.com/bootstrap-datetimepicker/assets/js/bootstrap-datetimepicker.min.js"> </script>
    
    
     <script type="text/javascript">
      
        $(document).ready(function() {
 	 $('#btnAdd').hide();
 	 $('#btnDel').hide(); 
        
$('#id_type').change(function() {
  if($('#id_type').val()!=2){
  	
 	 $('#btnAdd').hide();
 	 $('#btnDel').hide();  
  }
  else{
  console.log('2')
   	$('#btnAdd').fadeIn();
 	 $('#btnDel').fadeIn(); 
  
  }
});        
        
        
        
            $('#btnAdd').click(function() {
            var num = $('.applyq').length + 1;
				$('#questions').append(
  $('<input>')
    .attr("id", "q"+ num)
    .attr("name","q" + num)
	.attr("type","text")
    .addClass('applyq')
);
 $('#no_q').val(num)       ;       
 				});
 				
            $('#btnDel').click(function() {
            var num = $('.applyq').length;
            $('#q'+ num).remove()
            
            });

$('#id_start_time').wrap('<div id="dt1" class="input-append date"/>');
$('#id_end_time').wrap('<div id="dt2" class="input-append date"/>');
$('#id_start_time').after("<span class='add-on'><i data-time-icon='icon-time' data-date-icon='icon-calendar'></i></span>");
$('#id_end_time').after("<span class='add-on'><i data-time-icon='icon-time' data-date-icon='icon-calendar'></i></span>");


      $('#dt2').datetimepicker({
        format: 'yyyy-MM-dd hh:mm',
        language: 'en'
      });
      
            $('#dt1').datetimepicker({
        format: 'yyyy-MM-dd hh:mm',
        language: 'en'
      });

        });
    </script>
 
{% if message %}
<div class="alert">
  <button type="button" class="close" data-dismiss="alert">&times;</button>
  {{message}}
</div>
{% endif %}
<form id='uploadform' enctype="multipart/form-data" action='/client-dashboard/upload-test/' method='POST'>
{% csrf_token %}
{{form.as_p}}
<input id="no_q" name="no_q" type="hidden" value="0"></input>

    <div>
        <input type="button" id="btnAdd" value="MOAR! questions" />
        <input type="button" id="btnDel" value="less questions" />
    </div>
    <div id="questions" class="span4" style="padding:20px"></div>
        
    
    </div>
     
<input id='submit' type='submit' name='submit'>
</form>
 
 
</body>
{% endblock %}