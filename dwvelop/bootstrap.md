# Bootstrap notes

After bootstrap is complete, check the operState status via following endpoint:

Path: https://192.168.7.13/api/v1/release/servicepackages
Verb: GET

1. wait for items[0].status.operState.timeStamp to be non-null (operState.state field will be missing while timestamp is null)
2. wait for operState.state == "Healthy"

items[0].status.deploymentState.state should be "Enabled" when the bootstrap is complete.

## Example Response after successful installation

```json
{
    "metadata": {},
    "items": [
        {
            "status": {
                "operState": {
                    "state": "Healthy",
                    "timeStamp": "2025-10-17T19:07:16Z"
                },
                "deploymentState": {
                    "state": "Enabled",
                    "timeStamp": "2025-10-17T19:08:44Z"
                },
                "installState": {
                    "state": "Installed",
                    "timeStamp": "2025-10-17T19:01:22Z"
                },
                "version": "12.2.3.70",
            }
        }
    ]
}
```

## Example Response while installation is in progress:

```json
{
    "metadata": {},
    "items": [
        {
            "status": {
                "operState": {
                    "timeStamp": null
                },
                "deploymentState": {
                    "state": "Processing",
                    "timeStamp": "2025-10-17T19:02:19Z"
                },
                "installState": {
                    "state": "Installed",
                    "timeStamp": "2025-10-17T19:01:22Z"
                },
            }
        }
    ]
}
```

## Full Example Response while installation is in progress

```json
{
    "metadata": {},
    "items": [
        {
            "kind": "ServicePackage",
            "apiVersion": "case.cncf.io/v1",
            "metadata": {
                "name": "cisco-ndfc",
                "uid": "ab0b5afa-eaff-4a22-9902-24e23bdcab23",
                "resourceVersion": "11180",
                "generation": 14,
                "creationTimestamp": "2025-10-17T19:01:17Z",
                "finalizers": [
                    "spm.case.cncf.io/sp-protection"
                ],
                "managedFields": [
                    {
                        "manager": "firmwared.bin",
                        "operation": "Update",
                        "apiVersion": "case.cncf.io/v1",
                        "time": "2025-10-17T19:01:17Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:spec": {
                                ".": {},
                                "f:displayName": {},
                                "f:kubernetes": {
                                    ".": {},
                                    "f:type": {}
                                },
                                "f:name": {},
                                "f:releaseMeta": {},
                                "f:specsFormat": {},
                                "f:vendor": {},
                                "f:version": {}
                            },
                            "f:status": {
                                ".": {},
                                "f:adminAction": {},
                                "f:deploymentState": {},
                                "f:installState": {},
                                "f:operState": {}
                            }
                        }
                    },
                    {
                        "manager": "spm.bin",
                        "operation": "Update",
                        "apiVersion": "case.cncf.io/v1",
                        "time": "2025-10-17T19:02:19Z",
                        "fieldsType": "FieldsV1",
                        "fieldsV1": {
                            "f:metadata": {
                                "f:finalizers": {
                                    ".": {},
                                    "v:\"spm.case.cncf.io/sp-protection\"": {}
                                }
                            },
                            "f:spec": {
                                "f:enabled": {}
                            },
                            "f:status": {
                                "f:conditions": {},
                                "f:deploymentState": {
                                    "f:state": {},
                                    "f:timeStamp": {}
                                },
                                "f:installState": {
                                    "f:state": {},
                                    "f:timeStamp": {}
                                }
                            }
                        }
                    }
                ]
            },
            "spec": {
                "kubernetes": {
                    "type": "App"
                },
                "name": "ndfc",
                "vendor": "cisco",
                "version": "12.2.3.70",
                "displayName": "Nexus Dashboard Fabric Controller",
                "releaseMeta": {},
                "enabled": true,
                "specsFormat": "Plain"
            },
            "status": {
                "operState": {
                    "timeStamp": null
                },
                "deploymentState": {
                    "state": "Processing",
                    "timeStamp": "2025-10-17T19:02:19Z"
                },
                "installState": {
                    "state": "Installed",
                    "timeStamp": "2025-10-17T19:01:22Z"
                },
                "conditions": [
                    {
                        "state": "Installing",
                        "timeStamp": "2025-10-17T19:01:18Z"
                    },
                    {
                        "state": "Installed",
                        "timeStamp": "2025-10-17T19:01:22Z"
                    },
                    {
                        "state": "DependencyWait",
                        "timeStamp": "2025-10-17T19:01:22Z"
                    },
                    {
                        "state": "Disabled",
                        "timeStamp": "2025-10-17T19:01:22Z"
                    },
                    {
                        "state": "DependencyWait",
                        "timeStamp": "2025-10-17T19:01:22Z"
                    },
                    {
                        "state": "Disabled",
                        "timeStamp": "2025-10-17T19:01:23Z"
                    },
                    {
                        "state": "DependencyWait",
                        "timeStamp": "2025-10-17T19:01:23Z"
                    },
                    {
                        "state": "Disabled",
                        "timeStamp": "2025-10-17T19:01:24Z"
                    },
                    {
                        "state": "DependencyWait",
                        "timeStamp": "2025-10-17T19:01:24Z"
                    },
                    {
                        "state": "ProfileSelection",
                        "timeStamp": "2025-10-17T19:01:24Z"
                    },
                    {
                        "state": "SetupResourceEnforcement",
                        "timeStamp": "2025-10-17T19:02:15Z"
                    },
                    {
                        "state": "Processing",
                        "timeStamp": "2025-10-17T19:02:19Z"
                    }
                ],
                "adminAction": {
                    "createTime": null,
                    "lastUpdated": null
                }
            }
        }
    ]
}
```