openerp_announcement = function(instance) {
     instance.web.WebClient.include({
        show_application: function() {
            return $.when(this._super.apply(this, arguments));
        },
        _ab_location: function(dbuuid) {
            return;
        },
        show_annoucement_bar: function() {
            return;
        }
    });
};
