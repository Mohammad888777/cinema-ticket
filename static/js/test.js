

$("#show-comment-form").on("click",function(){
    console.log("OKAYYYY")
        $(".add-comment").fadeToggle(1000) 
})

function addCom(){
    
    const form=new FormData()
    const body=$("#comment-body").val()
    form.append("body",body)
    form.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val())



    const url="{% url 'movieDetail' movie.id %}"

    console.log(url)

    $.ajax({
        type:"POST",
        url:url,
        data:form,
        contentType: false,
        cache: false,
        processData:false,
        success:function(res){
            console.log(res)

            const profileImage=res[0].imageProfile
            const divToBeAdded=$("#add-comment-here")
            
            const newComment=`


                            <div class="mv-user-review-item">
                                <div class="user-infor">
                                    <img src="${profileImage}" alt="">
                                    <div>
                                        <h3>${res[0].body.slice(0,12)}</h3>
                                        <div class="no-star" >
                            
                                                {% ratings object %}
                                            
                                        </div>
                                        <p class="time">
                                            ${res[0].created}<a href="#"> ${res[0].username}</a>
                                        </p>
                                    </div>
                                </div>
                                <p>
                                    ${res[0].body}
                                </p>
                            </div>
            `
            divToBeAdded.append(newComment)
            $("#comment-body").val('')
        }

    })
        

}

