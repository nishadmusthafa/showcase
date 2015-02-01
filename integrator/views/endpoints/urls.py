from django.conf.urls import patterns, include, url
from views import ActionBridgeView, AgentView, AuthView, ContactView, InteractionView

urlpatterns = patterns('',
    url(r'^integrations/(?P<integration_id>\w+)/actions/(?P<action_id>\w+)/$',
        ActionBridgeView.as_view(),
        name='action_endpoint'),
    ##########################################################################
    # The below urls are commented as there is no UI implemented to configure#
    # these depending on a specific integrations. One such implementation    #
    # has been shown above for the purpose of the tech problem. My apologies #
    # for leaving this incomplete. I am a little hard pressed on time to     #
    # complete all the views. My main intention was to show a prototype of   #
    # action and Integration.                                                #
    ##########################################################################
    # url(r'^integrations/(?P<integration_id>\w+)/auth_validation/$',        #
    #     AuthView.as_view(),                                                #
    #     name='auth_validation_endpoint'),                                  #
    # url(r'^integrations/(?P<integration_id>\w+)/contact_sync/$',           #
    #     ContactView.as_view(),                                             #
    #     name='contact_sync_endpoint'),                                     #
    # url(r'^integrations/(?P<integration_id>\w+)/agent_sync/$',             #
    #     AgentView.as_view(),                                               #
    #     name='agent_sync_endpoint'),                                       #
    # url(r'^integrations/(?P<integration_id>\w+)/interaction_retrieval/$',  #
    #     InteractionView.as_view(),                                         #
    #     name='interaction_retrieval_endpoint'),                            #
    ##########################################################################
    # The following are very specific non general urls to solve the Talkdesk #
    # tech challenge                                                         #
    ##########################################################################
    url(r'^integrations/nishadhelpscout/auth_validation/$',
        AuthView.as_view(),
        name='auth_validation_endpoint'),
    url(r'^integrations/nishadhelpscout/contact_sync/$',
        ContactView.as_view(),
        name='contact_sync_endpoint'),
    url(r'^integrations/nishadhelpscout/agent_sync/$',
        AgentView.as_view(),
        name='agent_sync_endpoint'),
    url(r'^integrations/nishadhelpscout/interaction_retrieval/$',
        InteractionView.as_view(),
        name='interaction_endpoint'),
)
