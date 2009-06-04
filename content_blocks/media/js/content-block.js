/*
*	Content Block
*	A JS class and an initialization script for generating AJAX-based inline
*   editable content blocks
*	
*	Requires Trapeze jQuery library
*	
*	Taylan Pince (tpince at trapeze dot com) - June 4, 2009
*/


$.namespace("trapeze.ContentBlock");

trapeze.ContentBlock = $.Class.extend({

    container : null,

    process : function(response, status) {
        if (status == "success") {
            if ($(this.container).find("form").size() > 0) {
                this.init_form("", "success");
            } else {
                this.init_link();
            }
        } else {
            $(this.container).prepend("<p>There was an error with your request.</p>");
        }
    },

    submit_form : function() {
        $(this.container).load(
            $(this.container).find("form").attr("action"),
            $(this.container).find("form").serializeArray(),
            this.process.bind(this)
        );
        
        return false;
    },

    init_form : function(response, status) {
        if (status == "success") {
            $(this.container).find("textarea").focus();
            $(this.container).find("form").submit(this.submit_form.bind(this));
            $(this.container).find("a.content-block-cancel").click(this.cancel.bind(this));
        } else {
            $(this.container).prepend("<p>There was an error with your request.</p>");
        }
    },
    
    cancel : function() {
        $(this.container).load(
            $(this.container).find("form").attr("action"),
            "cancel",
            this.process.bind(this)
        );

        return false;
    },

    edit : function() {
        $(this.container).load(
            $(this.container).find("a.content-block-edit").attr("href"),
            null,
            this.init_form.bind(this)
        );

        return false;
    },
    
    init_link : function() {
        $(this.container).find("a.content-block-edit").click(this.edit.bind(this));
    },

    init : function(obj) {
        this.container = obj;

        this.init_link();
    }

});


$(function() {
    $("div.content_block").each(function() {
        new trapeze.ContentBlock(this);
    });
});
