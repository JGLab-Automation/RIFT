__author__ = 'JG'



from modules.automation.autobot.config.constants import constants as const

def project(proj_name, proj_desc):
    project = "{" \
            "\"rw-project:project\":" \
            "{" \
                "\"name\": \"{}\".format(proj_name)," \
                "\"description\": \"{}\".format(proj_desc)" \
            "}" \
          "}"

# project_config = "{" \
#                     "\"rw-project:project\": " \
#                         "{" \
#                             "\"name\": \"default\"," \
#                             "\"description\": \"Default project\"," \
#                             "\"project-config\": " \
#                                 "{" \
#                                     "\"user\": " \
#                                     "[" \
#                                         "{" \
#                                             "\"user-name\": \"admin\",\"user-domain\": \"system\"," \
#                                             "\"role\": [{\"role\": \"rw-project:project-admin\"}]" \
#                                         "}," \
#                                         "{" \
#                                             "\"user-name\": \"oper\",\"user-domain\": \"system\"," \
#                                             "\"role\": [{\"role\": \"rw-project:project-oper\"}]" \
#                                         "}" \
#                                     "]," \
#                                     "\"rw-umb-mgr:event-publish\":" \
#                                         "{" \
#                                             "\"event-publish-enable\": \"false\"" \
#                                         "}" \
#                                 "}" \
#                         "}" \
#                 "}"

# vim_os ="{" \
#             "\"rw-project:project\":" \
#                 "{" \
#                     "\"rw-cloud:cloud\":" \
#                         "{" \
#                             "\"account\":" \
#                                 "[" \
#                                     "{" \
#                                         "\"name\": \"{}\".format(cloud_name)," \
#                                         "\"account-type\": \"openstack\"," \
#                                         "\"openstack\":" \
#                                             "{" \
#                                                 "\"key\": \"{}\".format(const.vim_os_secret),
#                                                 \"secret\": \"{}\".format(const.vim_os_secret),
#                                                 \"auth_url\": \"{}\".format(const.vim_os_authURL),
#                                                 \"user-domain\": \"{}\".format(const.),
#                                                 \"project-domain\": \"{}\",
#                                                 \"tenant\": \"jghosh\",
#                                                 \"region\": \"RegionOne\",
#                                                 \"admin\": \"false\",
#                                                 \"mgmt-network\": \"private\",
#                                                 \"plugin-name\": \"rwcal_openstack\",
#                                                 \"dynamic-flavor-support\": \"true\",
#                                                 \"floating-ip-pool\": \"public\",
#                                                 \"cert-validate\": \"false\"" \
#                                             "}," \
#                                         "\"vdu-instance-timeout\": 300" \
#                                     "}" \
#                                 "]" \
#                         "}" \
#                 "}" \
#         "}"
