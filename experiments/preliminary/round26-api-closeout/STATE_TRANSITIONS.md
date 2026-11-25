# 变化前后与三个模块

状态=当前要求/事实/授权；决策=模型原始选择；执行/反馈=共同门禁、原生工具及后续状态。完整原话和SHA见两份代表轨迹。

## A_R_54_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "5669664287",
          "4900990404"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      {
        "kind": "scope",
        "source_ref": 9,
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval.",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "5669664287",
      "4900990404"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "5669664287",
          "4900990404"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "880.39",
      "epoch": 0,
      "fingerprint": "246df1c62f473a7f95395258d9941039e15282f783ee436a3e7803ac9003f0e8"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "4900990404",
      "9862136885"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "5669664287",
          "4900990404"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "880.39",
      "epoch": 0,
      "fingerprint": "246df1c62f473a7f95395258d9941039e15282f783ee436a3e7803ac9003f0e8"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  }
}
```
```json
{
  "event": 10,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 11,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      }
    ],
    "processed_refs": [
      11
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "4900990404",
      "9862136885"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "595.03",
      "epoch": 1,
      "fingerprint": "d900eb3984cacf36c4dd69f50cb79d852a8526fbf78275f22780fa5012ff1c07"
    },
    "authorization": null,
    "pending": [
      11
    ],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "4900990404",
      "9862136885"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "595.03",
      "epoch": 1,
      "fingerprint": "d900eb3984cacf36c4dd69f50cb79d852a8526fbf78275f22780fa5012ff1c07"
    },
    "authorization": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "epoch": 1,
      "source_ref": 11,
      "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
    },
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
      },
      {
        "source_ref": 11,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W4597054","parameters":{},"reason":"necessary current prerequisites program-verified","source":"program","work_type":"prepare"}`

## A_R_54_r2_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "5669664287",
          "4900990404"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      {
        "kind": "scope",
        "source_ref": 9,
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged.",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "5669664287",
      "4900990404"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "5669664287",
          "4900990404"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "880.39",
      "epoch": 0,
      "fingerprint": "246df1c62f473a7f95395258d9941039e15282f783ee436a3e7803ac9003f0e8"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "4900990404",
      "9862136885"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "5669664287",
          "4900990404"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "880.39",
      "epoch": 0,
      "fingerprint": "246df1c62f473a7f95395258d9941039e15282f783ee436a3e7803ac9003f0e8"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  }
}
```
```json
{
  "event": 10,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 11,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      }
    ],
    "processed_refs": [
      11
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "4900990404",
      "9862136885"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "595.03",
      "epoch": 1,
      "fingerprint": "d900eb3984cacf36c4dd69f50cb79d852a8526fbf78275f22780fa5012ff1c07"
    },
    "authorization": null,
    "pending": [
      11
    ],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "4900990404",
      "9862136885"
    ],
    "payment": "gift_card_3491931",
    "plan": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "refund_amount": "595.03",
      "epoch": 1,
      "fingerprint": "d900eb3984cacf36c4dd69f50cb79d852a8526fbf78275f22780fa5012ff1c07"
    },
    "authorization": {
      "arguments": {
        "order_id": "#W4597054",
        "item_ids": [
          "4900990404",
          "9862136885"
        ],
        "payment_method_id": "gift_card_3491931"
      },
      "epoch": 1,
      "source_ref": 11,
      "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
    },
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged."
      },
      {
        "source_ref": 11,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"4900990404\",\"9862136885\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W4597054","parameters":{},"reason":"necessary current prerequisites program-verified","source":"program","work_type":"prepare"}`

## A_R_73_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "3320557165",
          "2698416822"
        ],
        "payment_method_id": "credit_card_6824399"
      },
      {
        "kind": "scope",
        "source_ref": 9,
        "quote": "change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval.",
        "item_ids": [
          "2698416822",
          "8098621301"
        ],
        "payment_method_id": "credit_card_6824399"
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "3320557165",
      "2698416822"
    ],
    "payment": "credit_card_6824399",
    "plan": {
      "arguments": {
        "order_id": "#W5272531",
        "item_ids": [
          "3320557165",
          "2698416822"
        ],
        "payment_method_id": "credit_card_6824399"
      },
      "refund_amount": "338.12",
      "epoch": 0,
      "fingerprint": "e13cbc63c64894eda94cdc97575329ef4e8be917910d3dfb774c002b5d18b10c"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "2698416822",
      "8098621301"
    ],
    "payment": "credit_card_6824399",
    "plan": {
      "arguments": {
        "order_id": "#W5272531",
        "item_ids": [
          "3320557165",
          "2698416822"
        ],
        "payment_method_id": "credit_card_6824399"
      },
      "refund_amount": "338.12",
      "epoch": 0,
      "fingerprint": "e13cbc63c64894eda94cdc97575329ef4e8be917910d3dfb774c002b5d18b10c"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  }
}
```
```json
{
  "event": 10,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 11,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "2698416822",
          "8098621301"
        ],
        "payment_method_id": "credit_card_6824399"
      }
    ],
    "processed_refs": [
      11
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "2698416822",
      "8098621301"
    ],
    "payment": "credit_card_6824399",
    "plan": {
      "arguments": {
        "order_id": "#W5272531",
        "item_ids": [
          "2698416822",
          "8098621301"
        ],
        "payment_method_id": "credit_card_6824399"
      },
      "refund_amount": "341.60",
      "epoch": 1,
      "fingerprint": "3f055e088235d4cebc6f8567155da880607b64294174dc75f635f4e2e6903903"
    },
    "authorization": null,
    "pending": [
      11
    ],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "2698416822",
      "8098621301"
    ],
    "payment": "credit_card_6824399",
    "plan": {
      "arguments": {
        "order_id": "#W5272531",
        "item_ids": [
          "2698416822",
          "8098621301"
        ],
        "payment_method_id": "credit_card_6824399"
      },
      "refund_amount": "341.60",
      "epoch": 1,
      "fingerprint": "3f055e088235d4cebc6f8567155da880607b64294174dc75f635f4e2e6903903"
    },
    "authorization": {
      "arguments": {
        "order_id": "#W5272531",
        "item_ids": [
          "2698416822",
          "8098621301"
        ],
        "payment_method_id": "credit_card_6824399"
      },
      "epoch": 1,
      "source_ref": 11,
      "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
    },
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "scope",
        "quote": "change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
      },
      {
        "source_ref": 11,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "scope",
      "source_ref": 9,
      "text": "Before submission, change my return scope to EXACTLY [\"2698416822\",\"8098621301\"]. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W5272531","parameters":{},"reason":"necessary current prerequisites program-verified","source":"program","work_type":"prepare"}`

## A_R_82_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "9973034634",
          "5952720925"
        ],
        "payment_method_id": "gift_card_7250692"
      },
      {
        "kind": "withdrawal",
        "source_ref": 9,
        "quote": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now.",
        "item_ids": [],
        "payment_method_id": null
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "9973034634",
      "5952720925"
    ],
    "payment": "gift_card_7250692",
    "plan": {
      "arguments": {
        "order_id": "#W9571698",
        "item_ids": [
          "9973034634",
          "5952720925"
        ],
        "payment_method_id": "gift_card_7250692"
      },
      "refund_amount": "3110.51",
      "epoch": 0,
      "fingerprint": "1e42ed778aeb79ab80ce8adb98bdab2509ceb3904f4180083597b4603ffa44dc"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "withdraw",
      "source_ref": 9,
      "text": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "9973034634",
      "5952720925"
    ],
    "payment": "gift_card_7250692",
    "plan": {
      "arguments": {
        "order_id": "#W9571698",
        "item_ids": [
          "9973034634",
          "5952720925"
        ],
        "payment_method_id": "gift_card_7250692"
      },
      "refund_amount": "3110.51",
      "epoch": 0,
      "fingerprint": "1e42ed778aeb79ab80ce8adb98bdab2509ceb3904f4180083597b4603ffa44dc"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "withdrawal",
        "quote": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now."
      }
    ],
    "withdrawn": true,
    "stopped": false,
    "change": {
      "kind": "withdraw",
      "source_ref": 9,
      "text": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W9571698","parameters":{},"reason":"User withdrew the return request; stop without writing or silently restoring the old scope.","source":"decision_model","work_type":"stop"}`

## A_R_89_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "8590708195",
          "9690244451"
        ],
        "payment_method_id": "paypal_2417743"
      },
      {
        "kind": "withdrawal",
        "source_ref": 9,
        "quote": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now.",
        "item_ids": [],
        "payment_method_id": null
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "8590708195",
      "9690244451"
    ],
    "payment": "paypal_2417743",
    "plan": {
      "arguments": {
        "order_id": "#W4680753",
        "item_ids": [
          "8590708195",
          "9690244451"
        ],
        "payment_method_id": "paypal_2417743"
      },
      "refund_amount": "394.12",
      "epoch": 0,
      "fingerprint": "ac9ba0d2f4e123d6d04798bb3c76b35055f3481ffb9af1707582f217ad779831"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "withdraw",
      "source_ref": 9,
      "text": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "8590708195",
      "9690244451"
    ],
    "payment": "paypal_2417743",
    "plan": {
      "arguments": {
        "order_id": "#W4680753",
        "item_ids": [
          "8590708195",
          "9690244451"
        ],
        "payment_method_id": "paypal_2417743"
      },
      "refund_amount": "394.12",
      "epoch": 0,
      "fingerprint": "ac9ba0d2f4e123d6d04798bb3c76b35055f3481ffb9af1707582f217ad779831"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "withdrawal",
        "quote": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now."
      }
    ],
    "withdrawn": true,
    "stopped": false,
    "change": {
      "kind": "withdraw",
      "source_ref": 9,
      "text": "Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W4680753","parameters":{},"reason":"User withdrew the return request; stop without registering a reduced or old scope.","source":"decision_model","work_type":"stop"}`

## A_R_RDB01_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "credit_card_3362387"
      },
      {
        "kind": "refund_permission",
        "source_ref": 9,
        "quote": "change the refund method to gift_card_2259499",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "gift_card_2259499"
      },
      {
        "kind": "withdrawal",
        "source_ref": 9,
        "quote": "Old approval is withdrawn for this new proposal; ask for new complete approval.",
        "item_ids": [
          "6452271382",
          "7848293342"
        ]
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "6452271382",
      "7848293342"
    ],
    "payment": "credit_card_3362387",
    "plan": {
      "arguments": {
        "order_id": "#W1067251",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "credit_card_3362387"
      },
      "refund_amount": "1201.55",
      "epoch": 0,
      "fingerprint": "17c8681a2b73defa599d5d2a701565db6dbed1f3813916a363c5688e1fe0cfee"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "payment",
      "source_ref": 9,
      "text": "Before submission, change the refund method to gift_card_2259499. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "6452271382",
      "7848293342"
    ],
    "payment": "gift_card_2259499",
    "plan": {
      "arguments": {
        "order_id": "#W1067251",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "credit_card_3362387"
      },
      "refund_amount": "1201.55",
      "epoch": 0,
      "fingerprint": "17c8681a2b73defa599d5d2a701565db6dbed1f3813916a363c5688e1fe0cfee"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "refund_permission",
        "quote": "change the refund method to gift_card_2259499"
      },
      {
        "source_ref": 9,
        "kind": "withdrawal",
        "quote": "Old approval is withdrawn for this new proposal; ask for new complete approval."
      }
    ],
    "withdrawn": true,
    "stopped": false,
    "change": {
      "kind": "payment",
      "source_ref": 9,
      "text": "Before submission, change the refund method to gift_card_2259499. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W1067251","parameters":{},"reason":"Current state shows withdrawn=true and the latest requirement source explicitly withdraws the old approval and asks for a new proposal; stop rather than silently returning a reduced or old scope.","source":"decision_model","work_type":"stop"}`

## A_R_RDB01_r2_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "credit_card_3362387"
      },
      {
        "kind": "refund_permission",
        "source_ref": 9,
        "quote": "change the refund method to gift_card_2259499",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "gift_card_2259499"
      },
      {
        "kind": "withdrawal",
        "source_ref": 9,
        "quote": "Old approval is withdrawn for this new proposal; ask for new complete approval.",
        "item_ids": [
          "6452271382",
          "7848293342"
        ]
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "6452271382",
      "7848293342"
    ],
    "payment": "credit_card_3362387",
    "plan": {
      "arguments": {
        "order_id": "#W1067251",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "credit_card_3362387"
      },
      "refund_amount": "1201.55",
      "epoch": 0,
      "fingerprint": "17c8681a2b73defa599d5d2a701565db6dbed1f3813916a363c5688e1fe0cfee"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "payment",
      "source_ref": 9,
      "text": "Before submission, change the refund method to gift_card_2259499. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "6452271382",
      "7848293342"
    ],
    "payment": "gift_card_2259499",
    "plan": {
      "arguments": {
        "order_id": "#W1067251",
        "item_ids": [
          "6452271382",
          "7848293342"
        ],
        "payment_method_id": "credit_card_3362387"
      },
      "refund_amount": "1201.55",
      "epoch": 0,
      "fingerprint": "17c8681a2b73defa599d5d2a701565db6dbed1f3813916a363c5688e1fe0cfee"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "refund_permission",
        "quote": "change the refund method to gift_card_2259499"
      },
      {
        "source_ref": 9,
        "kind": "withdrawal",
        "quote": "Old approval is withdrawn for this new proposal; ask for new complete approval."
      }
    ],
    "withdrawn": true,
    "stopped": false,
    "change": {
      "kind": "payment",
      "source_ref": 9,
      "text": "Before submission, change the refund method to gift_card_2259499. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W1067251","parameters":{},"reason":"Current state shows withdrawn=true and the latest requirement source (ref 9) withdraws the old approval and asks for a new proposal with gift_card_2259499; the prior credit_card proposal is no longer authorized, so stop rather than silently reusing the old scope/method.","source":"decision_model","work_type":"stop"}`

## A_R_RDB02_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 8,
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.",
        "item_ids": [
          "9421195098",
          "4920090458"
        ],
        "payment_method_id": "paypal_6262583"
      },
      {
        "kind": "refund_permission",
        "source_ref": 9,
        "quote": "change the refund method to gift_card_3324938",
        "item_ids": [
          "9421195098",
          "4920090458"
        ],
        "payment_method_id": "gift_card_3324938"
      },
      {
        "kind": "withdrawal",
        "source_ref": 9,
        "quote": "Old approval is withdrawn for this new proposal; ask for new complete approval.",
        "item_ids": [
          "9421195098",
          "4920090458"
        ]
      }
    ],
    "processed_refs": [
      8,
      9
    ]
  },
  "before": {
    "business": "return",
    "scope": [
      "9421195098",
      "4920090458"
    ],
    "payment": "paypal_6262583",
    "plan": {
      "arguments": {
        "order_id": "#W1504875",
        "item_ids": [
          "9421195098",
          "4920090458"
        ],
        "payment_method_id": "paypal_6262583"
      },
      "refund_amount": "414.24",
      "epoch": 0,
      "fingerprint": "c0b072d2b498b03158c4f29ce4a8e25d27673080b419919b131b3f39c4f0b026"
    },
    "authorization": null,
    "pending": [
      8,
      9
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "kind": "payment",
      "source_ref": 9,
      "text": "Before submission, change the refund method to gift_card_3324938. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval."
    },
    "terminal_reason": null
  },
  "after": {
    "business": "return",
    "scope": [
      "9421195098",
      "4920090458"
    ],
    "payment": "gift_card_3324938",
    "plan": {
      "arguments": {
        "order_id": "#W1504875",
        "item_ids": [
          "9421195098",
          "4920090458"
        ],
        "payment_method_id": "paypal_6262583"
      },
      "refund_amount": "414.24",
      "epoch": 0,
      "fingerprint": "c0b072d2b498b03158c4f29ce4a8e25d27673080b419919b131b3f39c4f0b026"
    },
    "authorization": null,
    "pending": [],
    "parsed_history": [
      {
        "source_ref": 8,
        "kind": "approval",
        "quote": "Yes, I approve exactly that complete current return proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed."
      },
      {
        "source_ref": 9,
        "kind": "refund_permission",
        "quote": "change the refund method to gift_card_3324938"
      },
      {
        "source_ref": 9,
        "kind": "withdrawal",
        "quote": "Old approval is withdrawn for this new proposal; ask for new complete approval."
      }
    ],
    "withdrawn": true,
    "stopped": false,
    "change": {
      "kind": "payment",
      "source_ref": 9,
      "text": "Before submission, change the refund method to gift_card_3324938. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval."
    },
    "terminal_reason": null
  }
}
```
首个后续工作：`{"event":6,"object":"#W1504875","parameters":{},"reason":"Current state shows withdrawn=true and the latest requirement source explicitly withdraws the old approval for a new proposal; policy says stop on actual withdrawal and do not silently return a reduced or old scope.","source":"decision_model","work_type":"stop"}`

## A_E_EDB05_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 14
      }
    ],
    "processed_refs": [
      15
    ],
    "needs_clarification": false,
    "analysis": "User explicitly approves the complete combined exchange proposal from assistant ref 14, covering all listed items and payment method."
  },
  "before": {
    "targets": {
      "4875647558": "3951031513",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [
      15
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3951031513"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "19 bar",
          "capacity": "1.5L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  },
  "after": {
    "targets": {
      "4875647558": "3951031513",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3951031513"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "19 bar",
          "capacity": "1.5L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  }
}
```
```json
{
  "event": 8,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "permission",
        "source_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00.",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true
      }
    ],
    "processed_refs": [
      19
    ],
    "needs_clarification": false,
    "analysis": "User grants specification permission to replace original item 4875647558 with SKU 3709608322, conditional on stock and whole signed difference <= 10000.00; explicitly specification-only, not transaction approval. Other items unchanged."
  },
  "before": {
    "targets": {
      "4875647558": "3951031513",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [
      19
    ],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3951031513"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "19 bar",
          "capacity": "1.5L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  },
  "after": {
    "targets": {
      "4875647558": "3709608322",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      },
      {
        "kind": "permission",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3709608322"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "9 bar",
          "capacity": "2L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  }
}
```
```json
{
  "event": 13,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 23,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 22
      }
    ],
    "processed_refs": [
      23
    ],
    "needs_clarification": false,
    "analysis": "User explicitly approves the complete combined exchange proposal referenced by assistant_ref 22, covering all listed items and payment method."
  },
  "before": {
    "targets": {
      "4875647558": "3709608322",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3709608322",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3709608322",
          "options": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "new_price": 2744.7,
          "old_price": 2805.77,
          "difference": -61.07,
          "sources": [
            17
          ]
        }
      ],
      "difference": -66.4,
      "fingerprint": "148c688e12c051f257d2",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3709608322"
        ]
      ]
    },
    "pending": [
      23
    ],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      },
      {
        "kind": "permission",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3709608322"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:4875647558": {
          "value": -61.07,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            17
          ]
        },
        "total": {
          "value": -66.4,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            20
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "9 bar",
          "capacity": "2L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "new_price": 2744.7,
                "old_price": 2805.77,
                "difference": -61.07,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -66.4,
            "fingerprint": "148c688e12c051f257d2",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3709608322"
              ]
            ]
          },
          "source": 20
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 20,
          "changed_record_keys": []
        }
      ]
    }
  },
  "after": {
    "targets": {
      "4875647558": "3709608322",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3709608322",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3709608322",
          "options": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "new_price": 2744.7,
          "old_price": 2805.77,
          "difference": -61.07,
          "sources": [
            17
          ]
        }
      ],
      "difference": -66.4,
      "fingerprint": "148c688e12c051f257d2",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3709608322"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      },
      {
        "kind": "permission",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00."
      },
      {
        "user_ref": 23,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "current_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3709608322",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3709608322"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:4875647558": {
          "value": -61.07,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            17
          ]
        },
        "total": {
          "value": -66.4,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            20
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "de6e69d6bc50134bf81c",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            22,
            23
          ]
        },
        "authorization": {
          "value": "148c688e12c051f257d2",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            22,
            23
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "9 bar",
          "capacity": "2L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [
        {
          "fingerprint": "148c688e12c051f257d2",
          "user_ref": 23,
          "assistant_ref": 22,
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "difference": -66.4
        }
      ],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "new_price": 2744.7,
                "old_price": 2805.77,
                "difference": -61.07,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -66.4,
            "fingerprint": "148c688e12c051f257d2",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3709608322"
              ]
            ]
          },
          "source": 20
        },
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "new_price": 2744.7,
                "old_price": 2805.77,
                "difference": -61.07,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -66.4,
            "fingerprint": "148c688e12c051f257d2",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3709608322"
              ]
            ]
          },
          "source": 22
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 22,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 22,
          "changed_record_keys": []
        }
      ]
    }
  }
}
```
首个后续工作：`{"event":6,"object":"4875647558","parameters":{"variant_id":"3709608322"},"reason":"Exact requested replacement 3951031513 is out of stock, so no exact-match plan is feasible. Variant 3709608322 is observed available, within the signed whole-difference cap (whole_difference -66.40), and requires new user specification permission before it can be used.","source":"decision_model","work_type":"clarify"}`

## A_E_EDB05_r2_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 14
      }
    ],
    "processed_refs": [
      15
    ],
    "needs_clarification": false,
    "analysis": "User explicitly approves the complete combined exchange proposal from assistant_ref 14, covering all listed items and payment method."
  },
  "before": {
    "targets": {
      "4875647558": "3951031513",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [
      15
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3951031513"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "19 bar",
          "capacity": "1.5L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  },
  "after": {
    "targets": {
      "4875647558": "3951031513",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3951031513"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "19 bar",
          "capacity": "1.5L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  }
}
```
```json
{
  "event": 8,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "permission",
        "source_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00.",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true
      }
    ],
    "processed_refs": [
      19
    ],
    "needs_clarification": false,
    "analysis": "User grants specification permission to replace original item 4875647558 with SKU 3709608322, conditional on stock and whole signed difference <= 10000.00; explicitly specification-only, not final approval. Other items unchanged."
  },
  "before": {
    "targets": {
      "4875647558": "3951031513",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [
      19
    ],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3951031513"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "19 bar",
          "capacity": "1.5L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  },
  "after": {
    "targets": {
      "4875647558": "3709608322",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3951031513",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3951031513",
          "options": {
            "pressure": "19 bar",
            "capacity": "1.5L",
            "type": "automatic"
          },
          "new_price": 3289.46,
          "old_price": 2805.77,
          "difference": 483.69,
          "sources": [
            8
          ]
        }
      ],
      "difference": 478.36,
      "fingerprint": "aede05a2816f1afb3518",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3951031513"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      },
      {
        "kind": "permission",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3709608322"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:4875647558": {
          "value": 483.69,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 478.36,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "9 bar",
          "capacity": "2L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:4875647558"
          ]
        }
      ]
    }
  }
}
```
```json
{
  "event": 13,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 23,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 22
      }
    ],
    "processed_refs": [
      23
    ],
    "needs_clarification": false,
    "analysis": "User explicitly approves the complete combined exchange proposal referenced by assistant_ref 22, covering all listed items and payment method."
  },
  "before": {
    "targets": {
      "4875647558": "3709608322",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3709608322",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3709608322",
          "options": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "new_price": 2744.7,
          "old_price": 2805.77,
          "difference": -61.07,
          "sources": [
            17
          ]
        }
      ],
      "difference": -66.4,
      "fingerprint": "148c688e12c051f257d2",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3709608322"
        ]
      ]
    },
    "pending": [
      23
    ],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      },
      {
        "kind": "permission",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3709608322"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:4875647558": {
          "value": -61.07,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            17
          ]
        },
        "total": {
          "value": -66.4,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            20
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "d1cd21cd583746e87f32",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "aede05a2816f1afb3518",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "9 bar",
          "capacity": "2L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "new_price": 2744.7,
                "old_price": 2805.77,
                "difference": -61.07,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -66.4,
            "fingerprint": "148c688e12c051f257d2",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3709608322"
              ]
            ]
          },
          "source": 20
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 20,
          "changed_record_keys": []
        }
      ]
    }
  },
  "after": {
    "targets": {
      "4875647558": "3709608322",
      "2185126308": "8277474082"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1335809",
        "item_ids": [
          "4875647558",
          "2185126308"
        ],
        "new_item_ids": [
          "3709608322",
          "8277474082"
        ],
        "payment_method_id": "paypal_3728317"
      },
      "rows": [
        {
          "item_id": "2185126308",
          "new_item_id": "8277474082",
          "options": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "new_price": 236.57,
          "old_price": 241.9,
          "difference": -5.33,
          "sources": [
            10
          ]
        },
        {
          "item_id": "4875647558",
          "new_item_id": "3709608322",
          "options": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "new_price": 2744.7,
          "old_price": 2805.77,
          "difference": -61.07,
          "sources": [
            17
          ]
        }
      ],
      "difference": -66.4,
      "fingerprint": "148c688e12c051f257d2",
      "order_id": "#W1335809",
      "payment_method_id": "paypal_3728317",
      "pairs": [
        [
          "2185126308",
          "8277474082"
        ],
        [
          "4875647558",
          "3709608322"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3951031513",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      },
      {
        "kind": "permission",
        "item_id": "4875647558",
        "variant_id": "3709608322",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 4875647558 with SKU 3709608322, if in stock and whole signed difference <= 10000.00."
      },
      {
        "user_ref": 23,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "current_approval",
        "proposal": {
          "order_id": "#W1335809",
          "item_ids": [
            "4875647558",
            "2185126308"
          ],
          "new_item_ids": [
            "3709608322",
            "8277474082"
          ],
          "payment_method_id": "paypal_3728317"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"4354588079\"},\"official_result\":{\"name\":\"Espresso Machine\",\"product_id\":\"4354588079\",\"variants\":{\"1157853815\":{\"available\":true,\"item_id\":\"1157853815\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":3096.7},\"2190871011\":{\"available\":true,\"item_id\":\"2190871011\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3105.6},\"3379843752\":{\"available\":true,\"item_id\":\"3379843752\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":3203.76},\"3709608322\":{\"available\":true,\"item_id\":\"3709608322\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2744.7},\"3714494375\":{\"available\":true,\"item_id\":\"3714494375\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"manual\"},\"price\":2709.83},\"3815173328\":{\"available\":true,\"item_id\":\"3815173328\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2908.42},\"3951031513\":{\"available\":false,\"item_id\":\"3951031513\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":3289.46},\"4875647558\":{\"available\":false,\"item_id\":\"4875647558\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2805.77},\"5839483328\":{\"available\":false,\"item_id\":\"5839483328\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"15 bar\",\"type\":\"automatic\"},\"price\":2929.06},\"6200867091\":{\"available\":true,\"item_id\":\"6200867091\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"capsule\"},\"price\":2955.17},\"6242772310\":{\"available\":false,\"item_id\":\"6242772310\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"automatic\"},\"price\":2996.03},\"6324294385\":{\"available\":false,\"item_id\":\"6324294385\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"automatic\"},\"price\":2719.01},\"7407838442\":{\"available\":true,\"item_id\":\"7407838442\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":3081.91},\"7441167885\":{\"available\":false,\"item_id\":\"7441167885\",\"options\":{\"capacity\":\"1.5L\",\"pressure\":\"15 bar\",\"type\":\"capsule\"},\"price\":2866.37},\"7774234341\":{\"available\":true,\"item_id\":\"7774234341\",\"options\":{\"capacity\":\"2L\",\"pressure\":\"9 bar\",\"type\":\"manual\"},\"price\":2719.16},\"7806008610\":{\"available\":true,\"item_id\":\"7806008610\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"9 bar\",\"type\":\"capsule\"},\"price\":2742.67},\"9884666842\":{\"available\":true,\"item_id\":\"9884666842\",\"options\":{\"capacity\":\"1L\",\"pressure\":\"19 bar\",\"type\":\"manual\"},\"price\":2794.7}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "anya_lee_8315",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:anya_lee_8315": {
          "value": {
            "user_id": "anya_lee_8315",
            "name": {
              "first_name": "Anya",
              "last_name": "Lee"
            },
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "email": "anya.lee3013@example.com",
            "payment_methods": {
              "paypal_3728317": {
                "source": "paypal",
                "id": "paypal_3728317"
              }
            },
            "orders": [
              "#W3176007",
              "#W1335809",
              "#W2989580"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1335809": {
          "value": {
            "order_id": "#W1335809",
            "user_id": "anya_lee_8315",
            "address": {
              "address1": "912 Elm Avenue",
              "address2": "Suite 936",
              "city": "San Antonio",
              "country": "USA",
              "state": "TX",
              "zip": "78227"
            },
            "items": [
              {
                "name": "Espresso Machine",
                "product_id": "4354588079",
                "item_id": "4875647558",
                "price": 2805.77,
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                }
              },
              {
                "name": "Hiking Boots",
                "product_id": "7363354090",
                "item_id": "2185126308",
                "price": 241.9,
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                }
              },
              {
                "name": "Electric Kettle",
                "product_id": "1075968781",
                "item_id": "7602931732",
                "price": 153.25,
                "options": {
                  "capacity": "1L",
                  "material": "stainless steel",
                  "color": "black"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "465535118094"
                ],
                "item_ids": [
                  "4875647558",
                  "2185126308",
                  "7602931732"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3200.92,
                "payment_method_id": "paypal_3728317"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "4875647558",
            "2185126308"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_3728317",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:anya_lee_8315"
          ],
          "sources": [
            0
          ]
        },
        "requirement:4875647558": {
          "value": {
            "pressure": "9 bar",
            "capacity": "2L",
            "type": "automatic"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:2185126308": {
          "value": {
            "size": "12",
            "material": "leather",
            "waterproof": "yes"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:4354588079": {
          "value": {
            "name": "Espresso Machine",
            "product_id": "4354588079",
            "variants": {
              "3709608322": {
                "item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": true,
                "price": 2744.7
              },
              "7407838442": {
                "item_id": "7407838442",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 3081.91
              },
              "6324294385": {
                "item_id": "6324294385",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2719.01
              },
              "1157853815": {
                "item_id": "1157853815",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "capsule"
                },
                "available": true,
                "price": 3096.7
              },
              "2190871011": {
                "item_id": "2190871011",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "manual"
                },
                "available": true,
                "price": 3105.6
              },
              "3714494375": {
                "item_id": "3714494375",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2709.83
              },
              "4875647558": {
                "item_id": "4875647558",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2805.77
              },
              "7441167885": {
                "item_id": "7441167885",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": false,
                "price": 2866.37
              },
              "3815173328": {
                "item_id": "3815173328",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1.5L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2908.42
              },
              "5839483328": {
                "item_id": "5839483328",
                "options": {
                  "pressure": "15 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2929.06
              },
              "7806008610": {
                "item_id": "7806008610",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2742.67
              },
              "7774234341": {
                "item_id": "7774234341",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 2719.16
              },
              "3951031513": {
                "item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "available": false,
                "price": 3289.46
              },
              "6242772310": {
                "item_id": "6242772310",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "automatic"
                },
                "available": false,
                "price": 2996.03
              },
              "6200867091": {
                "item_id": "6200867091",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "capsule"
                },
                "available": true,
                "price": 2955.17
              },
              "9884666842": {
                "item_id": "9884666842",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1L",
                  "type": "manual"
                },
                "available": true,
                "price": 2794.7
              },
              "3379843752": {
                "item_id": "3379843752",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "2L",
                  "type": "manual"
                },
                "available": true,
                "price": 3203.76
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:7363354090": {
          "value": {
            "name": "Hiking Boots",
            "product_id": "7363354090",
            "variants": {
              "1615379700": {
                "item_id": "1615379700",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 253.89
              },
              "8106223139": {
                "item_id": "8106223139",
                "options": {
                  "size": "9",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 249.12
              },
              "2658930189": {
                "item_id": "2658930189",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 241.68
              },
              "3812493782": {
                "item_id": "3812493782",
                "options": {
                  "size": "7",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 244.34
              },
              "2648909398": {
                "item_id": "2648909398",
                "options": {
                  "size": "8",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 240.87
              },
              "4582956489": {
                "item_id": "4582956489",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 241.96
              },
              "7228247242": {
                "item_id": "7228247242",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 251.38
              },
              "2185126308": {
                "item_id": "2185126308",
                "options": {
                  "size": "10",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 241.9
              },
              "6159919747": {
                "item_id": "6159919747",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 259.75
              },
              "1437889264": {
                "item_id": "1437889264",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 258.09
              },
              "8277474082": {
                "item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "available": true,
                "price": 236.57
              },
              "6546364613": {
                "item_id": "6546364613",
                "options": {
                  "size": "11",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 231.43
              },
              "1262139877": {
                "item_id": "1262139877",
                "options": {
                  "size": "7",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.99
              },
              "6595128475": {
                "item_id": "6595128475",
                "options": {
                  "size": "9",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 237.65
              },
              "5676696062": {
                "item_id": "5676696062",
                "options": {
                  "size": "11",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": true,
                "price": 245.99
              },
              "4694984344": {
                "item_id": "4694984344",
                "options": {
                  "size": "12",
                  "material": "synthetic",
                  "waterproof": "yes"
                },
                "available": false,
                "price": 239.78
              },
              "3613716226": {
                "item_id": "3613716226",
                "options": {
                  "size": "8",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": true,
                "price": 253.54
              },
              "8118291112": {
                "item_id": "8118291112",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "no"
                },
                "available": false,
                "price": 260.56
              },
              "4127323219": {
                "item_id": "4127323219",
                "options": {
                  "size": "10",
                  "material": "synthetic",
                  "waterproof": "no"
                },
                "available": false,
                "price": 251.82
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:2185126308": {
          "value": [
            "8277474082"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "catalog:7363354090",
            "order:#W1335809"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:2185126308": {
          "value": -5.33,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:2185126308",
            "catalog:7363354090"
          ],
          "sources": [
            10
          ]
        },
        "match:4875647558": {
          "value": [
            "3709608322"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "catalog:4354588079",
            "order:#W1335809"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:4875647558": {
          "value": -61.07,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:4875647558",
            "catalog:4354588079"
          ],
          "sources": [
            17
          ]
        },
        "total": {
          "value": -66.4,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:4875647558",
            "delta:2185126308"
          ],
          "sources": [
            20
          ]
        },
        "confirmation:2185126308": {
          "value": "ba0411a73962d731987b",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:2185126308",
            "match:2185126308",
            "delta:2185126308"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:4875647558": {
          "value": "de6e69d6bc50134bf81c",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:4875647558",
            "match:4875647558",
            "delta:4875647558"
          ],
          "sources": [
            22,
            23
          ]
        },
        "authorization": {
          "value": "148c688e12c051f257d2",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:4875647558",
            "confirmation:2185126308"
          ],
          "sources": [
            22,
            23
          ]
        }
      },
      "product_refs": {
        "4354588079": 17,
        "7363354090": 10
      },
      "orders": {
        "#W1335809": {
          "order_id": "#W1335809",
          "user_id": "anya_lee_8315",
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "items": [
            {
              "name": "Espresso Machine",
              "product_id": "4354588079",
              "item_id": "4875647558",
              "price": 2805.77,
              "options": {
                "pressure": "15 bar",
                "capacity": "1L",
                "type": "capsule"
              }
            },
            {
              "name": "Hiking Boots",
              "product_id": "7363354090",
              "item_id": "2185126308",
              "price": 241.9,
              "options": {
                "size": "10",
                "material": "leather",
                "waterproof": "no"
              }
            },
            {
              "name": "Electric Kettle",
              "product_id": "1075968781",
              "item_id": "7602931732",
              "price": 153.25,
              "options": {
                "capacity": "1L",
                "material": "stainless steel",
                "color": "black"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "465535118094"
              ],
              "item_ids": [
                "4875647558",
                "2185126308",
                "7602931732"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3200.92,
              "payment_method_id": "paypal_3728317"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "anya_lee_8315": {
          "user_id": "anya_lee_8315",
          "name": {
            "first_name": "Anya",
            "last_name": "Lee"
          },
          "address": {
            "address1": "912 Elm Avenue",
            "address2": "Suite 936",
            "city": "San Antonio",
            "country": "USA",
            "state": "TX",
            "zip": "78227"
          },
          "email": "anya.lee3013@example.com",
          "payment_methods": {
            "paypal_3728317": {
              "source": "paypal",
              "id": "paypal_3728317"
            }
          },
          "orders": [
            "#W3176007",
            "#W1335809",
            "#W2989580"
          ]
        }
      },
      "evidence": {},
      "authenticated": "anya_lee_8315",
      "scope": [
        "4875647558",
        "2185126308"
      ],
      "requirements": {
        "4875647558": {
          "pressure": "9 bar",
          "capacity": "2L",
          "type": "automatic"
        },
        "2185126308": {
          "size": "12",
          "material": "leather",
          "waterproof": "yes"
        }
      },
      "old_confirmations": [
        {
          "fingerprint": "148c688e12c051f257d2",
          "user_ref": 23,
          "assistant_ref": 22,
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "difference": -66.4
        }
      ],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3951031513",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3951031513",
                "options": {
                  "pressure": "19 bar",
                  "capacity": "1.5L",
                  "type": "automatic"
                },
                "new_price": 3289.46,
                "old_price": 2805.77,
                "difference": 483.69,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 478.36,
            "fingerprint": "aede05a2816f1afb3518",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3951031513"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "new_price": 2744.7,
                "old_price": 2805.77,
                "difference": -61.07,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -66.4,
            "fingerprint": "148c688e12c051f257d2",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3709608322"
              ]
            ]
          },
          "source": 20
        },
        {
          "arguments": {
            "order_id": "#W1335809",
            "item_ids": [
              "4875647558",
              "2185126308"
            ],
            "new_item_ids": [
              "3709608322",
              "8277474082"
            ],
            "payment_method_id": "paypal_3728317"
          },
          "plan": {
            "rows": [
              {
                "item_id": "2185126308",
                "new_item_id": "8277474082",
                "options": {
                  "size": "12",
                  "material": "leather",
                  "waterproof": "yes"
                },
                "new_price": 236.57,
                "old_price": 241.9,
                "difference": -5.33,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "4875647558",
                "new_item_id": "3709608322",
                "options": {
                  "pressure": "9 bar",
                  "capacity": "2L",
                  "type": "automatic"
                },
                "new_price": 2744.7,
                "old_price": 2805.77,
                "difference": -61.07,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -66.4,
            "fingerprint": "148c688e12c051f257d2",
            "order_id": "#W1335809",
            "payment_method_id": "paypal_3728317",
            "pairs": [
              [
                "2185126308",
                "8277474082"
              ],
              [
                "4875647558",
                "3709608322"
              ]
            ]
          },
          "source": 22
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1335809",
      "payment": "paypal_3728317",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:2185126308"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:4875647558"
          ]
        },
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "2185126308"
          ],
          "source": 22,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4875647558"
          ],
          "source": 22,
          "changed_record_keys": []
        }
      ]
    }
  }
}
```
首个后续工作：`{"event":6,"object":"4875647558","parameters":{"variant_id":"3709608322"},"reason":"Current requested SKU 3951031513 is out of stock, so exact match is infeasible; variant 3709608322 is observed available within the signed cap and is the closest negotiable alternative (matches type automatic, only capacity/pressure differ), requiring new user specification permission.","source":"decision_model","work_type":"clarify"}`

## A_E_EDB06_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 14
      }
    ],
    "processed_refs": [
      15
    ],
    "needs_clarification": false,
    "analysis": "User explicitly approves the complete combined proposal from assistant_ref 14, covering all listed items and payment method."
  },
  "before": {
    "targets": {
      "6206533187": "5570660360",
      "4402162122": "3616838507"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1341845",
        "item_ids": [
          "6206533187",
          "4402162122"
        ],
        "new_item_ids": [
          "5570660360",
          "3616838507"
        ],
        "payment_method_id": "credit_card_6450164"
      },
      "rows": [
        {
          "item_id": "4402162122",
          "new_item_id": "3616838507",
          "options": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "new_price": 226.11,
          "old_price": 233.9,
          "difference": -7.79,
          "sources": [
            10
          ]
        },
        {
          "item_id": "6206533187",
          "new_item_id": "5570660360",
          "options": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "none"
          },
          "new_price": 51.54,
          "old_price": 47.83,
          "difference": 3.71,
          "sources": [
            8
          ]
        }
      ],
      "difference": -4.08,
      "fingerprint": "baa7d23a5b7ca58855d8",
      "order_id": "#W1341845",
      "payment_method_id": "credit_card_6450164",
      "pairs": [
        [
          "4402162122",
          "3616838507"
        ],
        [
          "6206533187",
          "5570660360"
        ]
      ]
    },
    "pending": [
      15
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"2696197613\"},\"official_result\":{\"name\":\"LED Light Bulb\",\"product_id\":\"2696197613\",\"variants\":{\"3034017579\":{\"available\":false,\"item_id\":\"3034017579\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"Wi-Fi\"},\"price\":49.72},\"4938013542\":{\"available\":true,\"item_id\":\"4938013542\",\"options\":{\"brightness\":\"100W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.2},\"5111440845\":{\"available\":true,\"item_id\":\"5111440845\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Bluetooth\"},\"price\":48.55},\"5570660360\":{\"available\":false,\"item_id\":\"5570660360\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"none\"},\"price\":51.54},\"6206533187\":{\"available\":false,\"item_id\":\"6206533187\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.83},\"7445824652\":{\"available\":true,\"item_id\":\"7445824652\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Wi-Fi\"},\"price\":49.8}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "yara_lee_7701",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:yara_lee_7701": {
          "value": {
            "user_id": "yara_lee_7701",
            "name": {
              "first_name": "Yara",
              "last_name": "Lee"
            },
            "address": {
              "address1": "944 Laurel Lane",
              "address2": "Suite 386",
              "city": "Houston",
              "country": "USA",
              "state": "TX",
              "zip": "77243"
            },
            "email": "yara.lee9368@example.com",
            "payment_methods": {
              "credit_card_6450164": {
                "source": "credit_card",
                "id": "credit_card_6450164",
                "brand": "visa",
                "last_four": "6367"
              },
              "credit_card_6680679": {
                "source": "credit_card",
                "id": "credit_card_6680679",
                "brand": "mastercard",
                "last_four": "5715"
              }
            },
            "orders": [
              "#W2832660",
              "#W1341845",
              "#W3320020"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1341845": {
          "value": {
            "order_id": "#W1341845",
            "user_id": "yara_lee_7701",
            "address": {
              "address1": "490 Highland Drive",
              "address2": "Suite 496",
              "city": "Fort Worth",
              "country": "USA",
              "state": "TX",
              "zip": "76153"
            },
            "items": [
              {
                "name": "LED Light Bulb",
                "product_id": "2696197613",
                "item_id": "6206533187",
                "price": 47.83,
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                }
              },
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "4402162122",
                "price": 233.9,
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                }
              },
              {
                "name": "Bluetooth Speaker",
                "product_id": "4768869376",
                "item_id": "6704763132",
                "price": 305.45,
                "options": {
                  "color": "blue",
                  "battery life": "10 hours",
                  "water resistance": "no"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "712388952344"
                ],
                "item_ids": [
                  "6206533187",
                  "4402162122",
                  "6704763132"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 587.18,
                "payment_method_id": "credit_card_6450164"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "6206533187",
            "4402162122"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "credit_card_6450164",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:yara_lee_7701"
          ],
          "sources": [
            0
          ]
        },
        "requirement:6206533187": {
          "value": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "none"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:4402162122": {
          "value": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:2696197613": {
          "value": {
            "name": "LED Light Bulb",
            "product_id": "2696197613",
            "variants": {
              "7445824652": {
                "item_id": "7445824652",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Wi-Fi"
                },
                "available": true,
                "price": 49.8
              },
              "3034017579": {
                "item_id": "3034017579",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "Wi-Fi"
                },
                "available": false,
                "price": 49.72
              },
              "5111440845": {
                "item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "available": true,
                "price": 48.55
              },
              "5570660360": {
                "item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "available": false,
                "price": 51.54
              },
              "6206533187": {
                "item_id": "6206533187",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": false,
                "price": 47.83
              },
              "4938013542": {
                "item_id": "4938013542",
                "options": {
                  "brightness": "100W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": true,
                "price": 47.2
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4402162122": {
          "value": [
            "3616838507"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "catalog:1656367028",
            "order:#W1341845"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4402162122": {
          "value": -7.79,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4402162122",
            "catalog:1656367028"
          ],
          "sources": [
            10
          ]
        },
        "match:6206533187": {
          "value": [
            "5570660360"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:6206533187",
            "catalog:2696197613",
            "order:#W1341845"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:6206533187": {
          "value": 3.71,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:6206533187",
            "catalog:2696197613"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": -4.08,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:6206533187",
            "delta:4402162122"
          ],
          "sources": [
            12
          ]
        }
      },
      "product_refs": {
        "2696197613": 17,
        "1656367028": 10
      },
      "orders": {
        "#W1341845": {
          "order_id": "#W1341845",
          "user_id": "yara_lee_7701",
          "address": {
            "address1": "490 Highland Drive",
            "address2": "Suite 496",
            "city": "Fort Worth",
            "country": "USA",
            "state": "TX",
            "zip": "76153"
          },
          "items": [
            {
              "name": "LED Light Bulb",
              "product_id": "2696197613",
              "item_id": "6206533187",
              "price": 47.83,
              "options": {
                "brightness": "75W equivalent",
                "color temperature": "warm white",
                "connectivity": "none"
              }
            },
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "4402162122",
              "price": 233.9,
              "options": {
                "switch type": "tactile",
                "backlight": "RGB",
                "size": "60%"
              }
            },
            {
              "name": "Bluetooth Speaker",
              "product_id": "4768869376",
              "item_id": "6704763132",
              "price": 305.45,
              "options": {
                "color": "blue",
                "battery life": "10 hours",
                "water resistance": "no"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "712388952344"
              ],
              "item_ids": [
                "6206533187",
                "4402162122",
                "6704763132"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 587.18,
              "payment_method_id": "credit_card_6450164"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "yara_lee_7701": {
          "user_id": "yara_lee_7701",
          "name": {
            "first_name": "Yara",
            "last_name": "Lee"
          },
          "address": {
            "address1": "944 Laurel Lane",
            "address2": "Suite 386",
            "city": "Houston",
            "country": "USA",
            "state": "TX",
            "zip": "77243"
          },
          "email": "yara.lee9368@example.com",
          "payment_methods": {
            "credit_card_6450164": {
              "source": "credit_card",
              "id": "credit_card_6450164",
              "brand": "visa",
              "last_four": "6367"
            },
            "credit_card_6680679": {
              "source": "credit_card",
              "id": "credit_card_6680679",
              "brand": "mastercard",
              "last_four": "5715"
            }
          },
          "orders": [
            "#W2832660",
            "#W1341845",
            "#W3320020"
          ]
        }
      },
      "evidence": {},
      "authenticated": "yara_lee_7701",
      "scope": [
        "6206533187",
        "4402162122"
      ],
      "requirements": {
        "6206533187": {
          "brightness": "60W equivalent",
          "color temperature": "daylight",
          "connectivity": "none"
        },
        "4402162122": {
          "switch type": "tactile",
          "backlight": "white",
          "size": "full size"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5570660360",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "new_price": 51.54,
                "old_price": 47.83,
                "difference": 3.71,
                "sources": [
                  8
                ]
              }
            ],
            "difference": -4.08,
            "fingerprint": "baa7d23a5b7ca58855d8",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5570660360"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1341845",
      "payment": "credit_card_6450164",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4402162122"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:6206533187"
          ]
        }
      ]
    }
  },
  "after": {
    "targets": {
      "6206533187": "5570660360",
      "4402162122": "3616838507"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1341845",
        "item_ids": [
          "6206533187",
          "4402162122"
        ],
        "new_item_ids": [
          "5570660360",
          "3616838507"
        ],
        "payment_method_id": "credit_card_6450164"
      },
      "rows": [
        {
          "item_id": "4402162122",
          "new_item_id": "3616838507",
          "options": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "new_price": 226.11,
          "old_price": 233.9,
          "difference": -7.79,
          "sources": [
            10
          ]
        },
        {
          "item_id": "6206533187",
          "new_item_id": "5570660360",
          "options": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "none"
          },
          "new_price": 51.54,
          "old_price": 47.83,
          "difference": 3.71,
          "sources": [
            8
          ]
        }
      ],
      "difference": -4.08,
      "fingerprint": "baa7d23a5b7ca58855d8",
      "order_id": "#W1341845",
      "payment_method_id": "credit_card_6450164",
      "pairs": [
        [
          "4402162122",
          "3616838507"
        ],
        [
          "6206533187",
          "5570660360"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1341845",
          "item_ids": [
            "6206533187",
            "4402162122"
          ],
          "new_item_ids": [
            "5570660360",
            "3616838507"
          ],
          "payment_method_id": "credit_card_6450164"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"2696197613\"},\"official_result\":{\"name\":\"LED Light Bulb\",\"product_id\":\"2696197613\",\"variants\":{\"3034017579\":{\"available\":false,\"item_id\":\"3034017579\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"Wi-Fi\"},\"price\":49.72},\"4938013542\":{\"available\":true,\"item_id\":\"4938013542\",\"options\":{\"brightness\":\"100W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.2},\"5111440845\":{\"available\":true,\"item_id\":\"5111440845\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Bluetooth\"},\"price\":48.55},\"5570660360\":{\"available\":false,\"item_id\":\"5570660360\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"none\"},\"price\":51.54},\"6206533187\":{\"available\":false,\"item_id\":\"6206533187\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.83},\"7445824652\":{\"available\":true,\"item_id\":\"7445824652\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Wi-Fi\"},\"price\":49.8}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "yara_lee_7701",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:yara_lee_7701": {
          "value": {
            "user_id": "yara_lee_7701",
            "name": {
              "first_name": "Yara",
              "last_name": "Lee"
            },
            "address": {
              "address1": "944 Laurel Lane",
              "address2": "Suite 386",
              "city": "Houston",
              "country": "USA",
              "state": "TX",
              "zip": "77243"
            },
            "email": "yara.lee9368@example.com",
            "payment_methods": {
              "credit_card_6450164": {
                "source": "credit_card",
                "id": "credit_card_6450164",
                "brand": "visa",
                "last_four": "6367"
              },
              "credit_card_6680679": {
                "source": "credit_card",
                "id": "credit_card_6680679",
                "brand": "mastercard",
                "last_four": "5715"
              }
            },
            "orders": [
              "#W2832660",
              "#W1341845",
              "#W3320020"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1341845": {
          "value": {
            "order_id": "#W1341845",
            "user_id": "yara_lee_7701",
            "address": {
              "address1": "490 Highland Drive",
              "address2": "Suite 496",
              "city": "Fort Worth",
              "country": "USA",
              "state": "TX",
              "zip": "76153"
            },
            "items": [
              {
                "name": "LED Light Bulb",
                "product_id": "2696197613",
                "item_id": "6206533187",
                "price": 47.83,
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                }
              },
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "4402162122",
                "price": 233.9,
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                }
              },
              {
                "name": "Bluetooth Speaker",
                "product_id": "4768869376",
                "item_id": "6704763132",
                "price": 305.45,
                "options": {
                  "color": "blue",
                  "battery life": "10 hours",
                  "water resistance": "no"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "712388952344"
                ],
                "item_ids": [
                  "6206533187",
                  "4402162122",
                  "6704763132"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 587.18,
                "payment_method_id": "credit_card_6450164"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "6206533187",
            "4402162122"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "credit_card_6450164",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:yara_lee_7701"
          ],
          "sources": [
            0
          ]
        },
        "requirement:6206533187": {
          "value": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "none"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:4402162122": {
          "value": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:2696197613": {
          "value": {
            "name": "LED Light Bulb",
            "product_id": "2696197613",
            "variants": {
              "7445824652": {
                "item_id": "7445824652",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Wi-Fi"
                },
                "available": true,
                "price": 49.8
              },
              "3034017579": {
                "item_id": "3034017579",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "Wi-Fi"
                },
                "available": false,
                "price": 49.72
              },
              "5111440845": {
                "item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "available": true,
                "price": 48.55
              },
              "5570660360": {
                "item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "available": false,
                "price": 51.54
              },
              "6206533187": {
                "item_id": "6206533187",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": false,
                "price": 47.83
              },
              "4938013542": {
                "item_id": "4938013542",
                "options": {
                  "brightness": "100W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": true,
                "price": 47.2
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4402162122": {
          "value": [
            "3616838507"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "catalog:1656367028",
            "order:#W1341845"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4402162122": {
          "value": -7.79,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4402162122",
            "catalog:1656367028"
          ],
          "sources": [
            10
          ]
        },
        "match:6206533187": {
          "value": [
            "5570660360"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:6206533187",
            "catalog:2696197613",
            "order:#W1341845"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:6206533187": {
          "value": 3.71,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:6206533187",
            "catalog:2696197613"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": -4.08,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:6206533187",
            "delta:4402162122"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:4402162122": {
          "value": "701719805a088f0b46f7",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "match:4402162122",
            "delta:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:6206533187": {
          "value": "29a1179698ed8e746771",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:6206533187",
            "match:6206533187",
            "delta:6206533187"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "baa7d23a5b7ca58855d8",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:6206533187",
            "confirmation:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "2696197613": 17,
        "1656367028": 10
      },
      "orders": {
        "#W1341845": {
          "order_id": "#W1341845",
          "user_id": "yara_lee_7701",
          "address": {
            "address1": "490 Highland Drive",
            "address2": "Suite 496",
            "city": "Fort Worth",
            "country": "USA",
            "state": "TX",
            "zip": "76153"
          },
          "items": [
            {
              "name": "LED Light Bulb",
              "product_id": "2696197613",
              "item_id": "6206533187",
              "price": 47.83,
              "options": {
                "brightness": "75W equivalent",
                "color temperature": "warm white",
                "connectivity": "none"
              }
            },
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "4402162122",
              "price": 233.9,
              "options": {
                "switch type": "tactile",
                "backlight": "RGB",
                "size": "60%"
              }
            },
            {
              "name": "Bluetooth Speaker",
              "product_id": "4768869376",
              "item_id": "6704763132",
              "price": 305.45,
              "options": {
                "color": "blue",
                "battery life": "10 hours",
                "water resistance": "no"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "712388952344"
              ],
              "item_ids": [
                "6206533187",
                "4402162122",
                "6704763132"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 587.18,
              "payment_method_id": "credit_card_6450164"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "yara_lee_7701": {
          "user_id": "yara_lee_7701",
          "name": {
            "first_name": "Yara",
            "last_name": "Lee"
          },
          "address": {
            "address1": "944 Laurel Lane",
            "address2": "Suite 386",
            "city": "Houston",
            "country": "USA",
            "state": "TX",
            "zip": "77243"
          },
          "email": "yara.lee9368@example.com",
          "payment_methods": {
            "credit_card_6450164": {
              "source": "credit_card",
              "id": "credit_card_6450164",
              "brand": "visa",
              "last_four": "6367"
            },
            "credit_card_6680679": {
              "source": "credit_card",
              "id": "credit_card_6680679",
              "brand": "mastercard",
              "last_four": "5715"
            }
          },
          "orders": [
            "#W2832660",
            "#W1341845",
            "#W3320020"
          ]
        }
      },
      "evidence": {},
      "authenticated": "yara_lee_7701",
      "scope": [
        "6206533187",
        "4402162122"
      ],
      "requirements": {
        "6206533187": {
          "brightness": "60W equivalent",
          "color temperature": "daylight",
          "connectivity": "none"
        },
        "4402162122": {
          "switch type": "tactile",
          "backlight": "white",
          "size": "full size"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5570660360",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "new_price": 51.54,
                "old_price": 47.83,
                "difference": 3.71,
                "sources": [
                  8
                ]
              }
            ],
            "difference": -4.08,
            "fingerprint": "baa7d23a5b7ca58855d8",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5570660360"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1341845",
      "payment": "credit_card_6450164",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4402162122"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:6206533187"
          ]
        }
      ]
    }
  }
}
```
```json
{
  "event": 8,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "permission",
        "source_ref": 19,
        "quote": "Replace my CURRENT request for original item 6206533187 with SKU 5111440845, if in stock and whole signed difference <= 10000.00.",
        "item_id": "6206533187",
        "variant_id": "5111440845",
        "conditional_stock": true
      }
    ],
    "processed_refs": [
      19
    ],
    "needs_clarification": false,
    "analysis": "User grants conditional specification permission to replace the current target for original item 6206533187 with SKU 5111440845, contingent on stock and whole signed difference cap; explicitly specification-only, not final approval. Other items unchanged."
  },
  "before": {
    "targets": {
      "6206533187": "5570660360",
      "4402162122": "3616838507"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1341845",
        "item_ids": [
          "6206533187",
          "4402162122"
        ],
        "new_item_ids": [
          "5570660360",
          "3616838507"
        ],
        "payment_method_id": "credit_card_6450164"
      },
      "rows": [
        {
          "item_id": "4402162122",
          "new_item_id": "3616838507",
          "options": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "new_price": 226.11,
          "old_price": 233.9,
          "difference": -7.79,
          "sources": [
            10
          ]
        },
        {
          "item_id": "6206533187",
          "new_item_id": "5570660360",
          "options": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "none"
          },
          "new_price": 51.54,
          "old_price": 47.83,
          "difference": 3.71,
          "sources": [
            8
          ]
        }
      ],
      "difference": -4.08,
      "fingerprint": "baa7d23a5b7ca58855d8",
      "order_id": "#W1341845",
      "payment_method_id": "credit_card_6450164",
      "pairs": [
        [
          "4402162122",
          "3616838507"
        ],
        [
          "6206533187",
          "5570660360"
        ]
      ]
    },
    "pending": [
      19
    ],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1341845",
          "item_ids": [
            "6206533187",
            "4402162122"
          ],
          "new_item_ids": [
            "5570660360",
            "3616838507"
          ],
          "payment_method_id": "credit_card_6450164"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"2696197613\"},\"official_result\":{\"name\":\"LED Light Bulb\",\"product_id\":\"2696197613\",\"variants\":{\"3034017579\":{\"available\":false,\"item_id\":\"3034017579\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"Wi-Fi\"},\"price\":49.72},\"4938013542\":{\"available\":true,\"item_id\":\"4938013542\",\"options\":{\"brightness\":\"100W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.2},\"5111440845\":{\"available\":true,\"item_id\":\"5111440845\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Bluetooth\"},\"price\":48.55},\"5570660360\":{\"available\":false,\"item_id\":\"5570660360\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"none\"},\"price\":51.54},\"6206533187\":{\"available\":false,\"item_id\":\"6206533187\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.83},\"7445824652\":{\"available\":true,\"item_id\":\"7445824652\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Wi-Fi\"},\"price\":49.8}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "yara_lee_7701",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:yara_lee_7701": {
          "value": {
            "user_id": "yara_lee_7701",
            "name": {
              "first_name": "Yara",
              "last_name": "Lee"
            },
            "address": {
              "address1": "944 Laurel Lane",
              "address2": "Suite 386",
              "city": "Houston",
              "country": "USA",
              "state": "TX",
              "zip": "77243"
            },
            "email": "yara.lee9368@example.com",
            "payment_methods": {
              "credit_card_6450164": {
                "source": "credit_card",
                "id": "credit_card_6450164",
                "brand": "visa",
                "last_four": "6367"
              },
              "credit_card_6680679": {
                "source": "credit_card",
                "id": "credit_card_6680679",
                "brand": "mastercard",
                "last_four": "5715"
              }
            },
            "orders": [
              "#W2832660",
              "#W1341845",
              "#W3320020"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1341845": {
          "value": {
            "order_id": "#W1341845",
            "user_id": "yara_lee_7701",
            "address": {
              "address1": "490 Highland Drive",
              "address2": "Suite 496",
              "city": "Fort Worth",
              "country": "USA",
              "state": "TX",
              "zip": "76153"
            },
            "items": [
              {
                "name": "LED Light Bulb",
                "product_id": "2696197613",
                "item_id": "6206533187",
                "price": 47.83,
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                }
              },
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "4402162122",
                "price": 233.9,
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                }
              },
              {
                "name": "Bluetooth Speaker",
                "product_id": "4768869376",
                "item_id": "6704763132",
                "price": 305.45,
                "options": {
                  "color": "blue",
                  "battery life": "10 hours",
                  "water resistance": "no"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "712388952344"
                ],
                "item_ids": [
                  "6206533187",
                  "4402162122",
                  "6704763132"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 587.18,
                "payment_method_id": "credit_card_6450164"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "6206533187",
            "4402162122"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "credit_card_6450164",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:yara_lee_7701"
          ],
          "sources": [
            0
          ]
        },
        "requirement:6206533187": {
          "value": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "none"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:4402162122": {
          "value": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:2696197613": {
          "value": {
            "name": "LED Light Bulb",
            "product_id": "2696197613",
            "variants": {
              "7445824652": {
                "item_id": "7445824652",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Wi-Fi"
                },
                "available": true,
                "price": 49.8
              },
              "3034017579": {
                "item_id": "3034017579",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "Wi-Fi"
                },
                "available": false,
                "price": 49.72
              },
              "5111440845": {
                "item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "available": true,
                "price": 48.55
              },
              "5570660360": {
                "item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "available": false,
                "price": 51.54
              },
              "6206533187": {
                "item_id": "6206533187",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": false,
                "price": 47.83
              },
              "4938013542": {
                "item_id": "4938013542",
                "options": {
                  "brightness": "100W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": true,
                "price": 47.2
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4402162122": {
          "value": [
            "3616838507"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "catalog:1656367028",
            "order:#W1341845"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4402162122": {
          "value": -7.79,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4402162122",
            "catalog:1656367028"
          ],
          "sources": [
            10
          ]
        },
        "match:6206533187": {
          "value": [
            "5570660360"
          ],
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:6206533187",
            "catalog:2696197613",
            "order:#W1341845"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:6206533187": {
          "value": 3.71,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:6206533187",
            "catalog:2696197613"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": -4.08,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:6206533187",
            "delta:4402162122"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:4402162122": {
          "value": "701719805a088f0b46f7",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "match:4402162122",
            "delta:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:6206533187": {
          "value": "29a1179698ed8e746771",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:6206533187",
            "match:6206533187",
            "delta:6206533187"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "baa7d23a5b7ca58855d8",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:6206533187",
            "confirmation:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "2696197613": 17,
        "1656367028": 10
      },
      "orders": {
        "#W1341845": {
          "order_id": "#W1341845",
          "user_id": "yara_lee_7701",
          "address": {
            "address1": "490 Highland Drive",
            "address2": "Suite 496",
            "city": "Fort Worth",
            "country": "USA",
            "state": "TX",
            "zip": "76153"
          },
          "items": [
            {
              "name": "LED Light Bulb",
              "product_id": "2696197613",
              "item_id": "6206533187",
              "price": 47.83,
              "options": {
                "brightness": "75W equivalent",
                "color temperature": "warm white",
                "connectivity": "none"
              }
            },
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "4402162122",
              "price": 233.9,
              "options": {
                "switch type": "tactile",
                "backlight": "RGB",
                "size": "60%"
              }
            },
            {
              "name": "Bluetooth Speaker",
              "product_id": "4768869376",
              "item_id": "6704763132",
              "price": 305.45,
              "options": {
                "color": "blue",
                "battery life": "10 hours",
                "water resistance": "no"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "712388952344"
              ],
              "item_ids": [
                "6206533187",
                "4402162122",
                "6704763132"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 587.18,
              "payment_method_id": "credit_card_6450164"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "yara_lee_7701": {
          "user_id": "yara_lee_7701",
          "name": {
            "first_name": "Yara",
            "last_name": "Lee"
          },
          "address": {
            "address1": "944 Laurel Lane",
            "address2": "Suite 386",
            "city": "Houston",
            "country": "USA",
            "state": "TX",
            "zip": "77243"
          },
          "email": "yara.lee9368@example.com",
          "payment_methods": {
            "credit_card_6450164": {
              "source": "credit_card",
              "id": "credit_card_6450164",
              "brand": "visa",
              "last_four": "6367"
            },
            "credit_card_6680679": {
              "source": "credit_card",
              "id": "credit_card_6680679",
              "brand": "mastercard",
              "last_four": "5715"
            }
          },
          "orders": [
            "#W2832660",
            "#W1341845",
            "#W3320020"
          ]
        }
      },
      "evidence": {},
      "authenticated": "yara_lee_7701",
      "scope": [
        "6206533187",
        "4402162122"
      ],
      "requirements": {
        "6206533187": {
          "brightness": "60W equivalent",
          "color temperature": "daylight",
          "connectivity": "none"
        },
        "4402162122": {
          "switch type": "tactile",
          "backlight": "white",
          "size": "full size"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5570660360",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "new_price": 51.54,
                "old_price": 47.83,
                "difference": 3.71,
                "sources": [
                  8
                ]
              }
            ],
            "difference": -4.08,
            "fingerprint": "baa7d23a5b7ca58855d8",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5570660360"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1341845",
      "payment": "credit_card_6450164",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4402162122"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:6206533187"
          ]
        }
      ]
    }
  },
  "after": {
    "targets": {
      "6206533187": "5111440845",
      "4402162122": "3616838507"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1341845",
        "item_ids": [
          "6206533187",
          "4402162122"
        ],
        "new_item_ids": [
          "5570660360",
          "3616838507"
        ],
        "payment_method_id": "credit_card_6450164"
      },
      "rows": [
        {
          "item_id": "4402162122",
          "new_item_id": "3616838507",
          "options": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "new_price": 226.11,
          "old_price": 233.9,
          "difference": -7.79,
          "sources": [
            10
          ]
        },
        {
          "item_id": "6206533187",
          "new_item_id": "5570660360",
          "options": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "none"
          },
          "new_price": 51.54,
          "old_price": 47.83,
          "difference": 3.71,
          "sources": [
            8
          ]
        }
      ],
      "difference": -4.08,
      "fingerprint": "baa7d23a5b7ca58855d8",
      "order_id": "#W1341845",
      "payment_method_id": "credit_card_6450164",
      "pairs": [
        [
          "4402162122",
          "3616838507"
        ],
        [
          "6206533187",
          "5570660360"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1341845",
          "item_ids": [
            "6206533187",
            "4402162122"
          ],
          "new_item_ids": [
            "5570660360",
            "3616838507"
          ],
          "payment_method_id": "credit_card_6450164"
        }
      },
      {
        "kind": "permission",
        "item_id": "6206533187",
        "variant_id": "5111440845",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 6206533187 with SKU 5111440845, if in stock and whole signed difference <= 10000.00."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"2696197613\"},\"official_result\":{\"name\":\"LED Light Bulb\",\"product_id\":\"2696197613\",\"variants\":{\"3034017579\":{\"available\":false,\"item_id\":\"3034017579\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"Wi-Fi\"},\"price\":49.72},\"4938013542\":{\"available\":true,\"item_id\":\"4938013542\",\"options\":{\"brightness\":\"100W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.2},\"5111440845\":{\"available\":true,\"item_id\":\"5111440845\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Bluetooth\"},\"price\":48.55},\"5570660360\":{\"available\":false,\"item_id\":\"5570660360\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"none\"},\"price\":51.54},\"6206533187\":{\"available\":false,\"item_id\":\"6206533187\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.83},\"7445824652\":{\"available\":true,\"item_id\":\"7445824652\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Wi-Fi\"},\"price\":49.8}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "yara_lee_7701",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:yara_lee_7701": {
          "value": {
            "user_id": "yara_lee_7701",
            "name": {
              "first_name": "Yara",
              "last_name": "Lee"
            },
            "address": {
              "address1": "944 Laurel Lane",
              "address2": "Suite 386",
              "city": "Houston",
              "country": "USA",
              "state": "TX",
              "zip": "77243"
            },
            "email": "yara.lee9368@example.com",
            "payment_methods": {
              "credit_card_6450164": {
                "source": "credit_card",
                "id": "credit_card_6450164",
                "brand": "visa",
                "last_four": "6367"
              },
              "credit_card_6680679": {
                "source": "credit_card",
                "id": "credit_card_6680679",
                "brand": "mastercard",
                "last_four": "5715"
              }
            },
            "orders": [
              "#W2832660",
              "#W1341845",
              "#W3320020"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1341845": {
          "value": {
            "order_id": "#W1341845",
            "user_id": "yara_lee_7701",
            "address": {
              "address1": "490 Highland Drive",
              "address2": "Suite 496",
              "city": "Fort Worth",
              "country": "USA",
              "state": "TX",
              "zip": "76153"
            },
            "items": [
              {
                "name": "LED Light Bulb",
                "product_id": "2696197613",
                "item_id": "6206533187",
                "price": 47.83,
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                }
              },
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "4402162122",
                "price": 233.9,
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                }
              },
              {
                "name": "Bluetooth Speaker",
                "product_id": "4768869376",
                "item_id": "6704763132",
                "price": 305.45,
                "options": {
                  "color": "blue",
                  "battery life": "10 hours",
                  "water resistance": "no"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "712388952344"
                ],
                "item_ids": [
                  "6206533187",
                  "4402162122",
                  "6704763132"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 587.18,
                "payment_method_id": "credit_card_6450164"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "6206533187",
            "4402162122"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "credit_card_6450164",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:yara_lee_7701"
          ],
          "sources": [
            0
          ]
        },
        "requirement:6206533187": {
          "value": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "Bluetooth"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:4402162122": {
          "value": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:2696197613": {
          "value": {
            "name": "LED Light Bulb",
            "product_id": "2696197613",
            "variants": {
              "7445824652": {
                "item_id": "7445824652",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Wi-Fi"
                },
                "available": true,
                "price": 49.8
              },
              "3034017579": {
                "item_id": "3034017579",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "Wi-Fi"
                },
                "available": false,
                "price": 49.72
              },
              "5111440845": {
                "item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "available": true,
                "price": 48.55
              },
              "5570660360": {
                "item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "available": false,
                "price": 51.54
              },
              "6206533187": {
                "item_id": "6206533187",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": false,
                "price": 47.83
              },
              "4938013542": {
                "item_id": "4938013542",
                "options": {
                  "brightness": "100W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": true,
                "price": 47.2
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4402162122": {
          "value": [
            "3616838507"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "catalog:1656367028",
            "order:#W1341845"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4402162122": {
          "value": -7.79,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4402162122",
            "catalog:1656367028"
          ],
          "sources": [
            10
          ]
        },
        "match:6206533187": {
          "value": [
            "5111440845"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:6206533187",
            "catalog:2696197613",
            "order:#W1341845"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:6206533187": {
          "value": 3.71,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:6206533187",
            "catalog:2696197613"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": -4.08,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:6206533187",
            "delta:4402162122"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:4402162122": {
          "value": "701719805a088f0b46f7",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "match:4402162122",
            "delta:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:6206533187": {
          "value": "29a1179698ed8e746771",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:6206533187",
            "match:6206533187",
            "delta:6206533187"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "baa7d23a5b7ca58855d8",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:6206533187",
            "confirmation:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "2696197613": 17,
        "1656367028": 10
      },
      "orders": {
        "#W1341845": {
          "order_id": "#W1341845",
          "user_id": "yara_lee_7701",
          "address": {
            "address1": "490 Highland Drive",
            "address2": "Suite 496",
            "city": "Fort Worth",
            "country": "USA",
            "state": "TX",
            "zip": "76153"
          },
          "items": [
            {
              "name": "LED Light Bulb",
              "product_id": "2696197613",
              "item_id": "6206533187",
              "price": 47.83,
              "options": {
                "brightness": "75W equivalent",
                "color temperature": "warm white",
                "connectivity": "none"
              }
            },
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "4402162122",
              "price": 233.9,
              "options": {
                "switch type": "tactile",
                "backlight": "RGB",
                "size": "60%"
              }
            },
            {
              "name": "Bluetooth Speaker",
              "product_id": "4768869376",
              "item_id": "6704763132",
              "price": 305.45,
              "options": {
                "color": "blue",
                "battery life": "10 hours",
                "water resistance": "no"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "712388952344"
              ],
              "item_ids": [
                "6206533187",
                "4402162122",
                "6704763132"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 587.18,
              "payment_method_id": "credit_card_6450164"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "yara_lee_7701": {
          "user_id": "yara_lee_7701",
          "name": {
            "first_name": "Yara",
            "last_name": "Lee"
          },
          "address": {
            "address1": "944 Laurel Lane",
            "address2": "Suite 386",
            "city": "Houston",
            "country": "USA",
            "state": "TX",
            "zip": "77243"
          },
          "email": "yara.lee9368@example.com",
          "payment_methods": {
            "credit_card_6450164": {
              "source": "credit_card",
              "id": "credit_card_6450164",
              "brand": "visa",
              "last_four": "6367"
            },
            "credit_card_6680679": {
              "source": "credit_card",
              "id": "credit_card_6680679",
              "brand": "mastercard",
              "last_four": "5715"
            }
          },
          "orders": [
            "#W2832660",
            "#W1341845",
            "#W3320020"
          ]
        }
      },
      "evidence": {},
      "authenticated": "yara_lee_7701",
      "scope": [
        "6206533187",
        "4402162122"
      ],
      "requirements": {
        "6206533187": {
          "brightness": "60W equivalent",
          "color temperature": "daylight",
          "connectivity": "Bluetooth"
        },
        "4402162122": {
          "switch type": "tactile",
          "backlight": "white",
          "size": "full size"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5570660360",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "new_price": 51.54,
                "old_price": 47.83,
                "difference": 3.71,
                "sources": [
                  8
                ]
              }
            ],
            "difference": -4.08,
            "fingerprint": "baa7d23a5b7ca58855d8",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5570660360"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1341845",
      "payment": "credit_card_6450164",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4402162122"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:6206533187"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:6206533187"
          ]
        }
      ]
    }
  }
}
```
```json
{
  "event": 13,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 23,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 22
      }
    ],
    "processed_refs": [
      23
    ],
    "needs_clarification": false,
    "analysis": "User explicitly approves the complete combined proposal referenced by assistant_ref 22."
  },
  "before": {
    "targets": {
      "6206533187": "5111440845",
      "4402162122": "3616838507"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1341845",
        "item_ids": [
          "6206533187",
          "4402162122"
        ],
        "new_item_ids": [
          "5111440845",
          "3616838507"
        ],
        "payment_method_id": "credit_card_6450164"
      },
      "rows": [
        {
          "item_id": "4402162122",
          "new_item_id": "3616838507",
          "options": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "new_price": 226.11,
          "old_price": 233.9,
          "difference": -7.79,
          "sources": [
            10
          ]
        },
        {
          "item_id": "6206533187",
          "new_item_id": "5111440845",
          "options": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "Bluetooth"
          },
          "new_price": 48.55,
          "old_price": 47.83,
          "difference": 0.72,
          "sources": [
            17
          ]
        }
      ],
      "difference": -7.07,
      "fingerprint": "e0a00c118f81b5daf923",
      "order_id": "#W1341845",
      "payment_method_id": "credit_card_6450164",
      "pairs": [
        [
          "4402162122",
          "3616838507"
        ],
        [
          "6206533187",
          "5111440845"
        ]
      ]
    },
    "pending": [
      23
    ],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1341845",
          "item_ids": [
            "6206533187",
            "4402162122"
          ],
          "new_item_ids": [
            "5570660360",
            "3616838507"
          ],
          "payment_method_id": "credit_card_6450164"
        }
      },
      {
        "kind": "permission",
        "item_id": "6206533187",
        "variant_id": "5111440845",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 6206533187 with SKU 5111440845, if in stock and whole signed difference <= 10000.00."
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"2696197613\"},\"official_result\":{\"name\":\"LED Light Bulb\",\"product_id\":\"2696197613\",\"variants\":{\"3034017579\":{\"available\":false,\"item_id\":\"3034017579\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"Wi-Fi\"},\"price\":49.72},\"4938013542\":{\"available\":true,\"item_id\":\"4938013542\",\"options\":{\"brightness\":\"100W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.2},\"5111440845\":{\"available\":true,\"item_id\":\"5111440845\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Bluetooth\"},\"price\":48.55},\"5570660360\":{\"available\":false,\"item_id\":\"5570660360\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"none\"},\"price\":51.54},\"6206533187\":{\"available\":false,\"item_id\":\"6206533187\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.83},\"7445824652\":{\"available\":true,\"item_id\":\"7445824652\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Wi-Fi\"},\"price\":49.8}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "yara_lee_7701",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:yara_lee_7701": {
          "value": {
            "user_id": "yara_lee_7701",
            "name": {
              "first_name": "Yara",
              "last_name": "Lee"
            },
            "address": {
              "address1": "944 Laurel Lane",
              "address2": "Suite 386",
              "city": "Houston",
              "country": "USA",
              "state": "TX",
              "zip": "77243"
            },
            "email": "yara.lee9368@example.com",
            "payment_methods": {
              "credit_card_6450164": {
                "source": "credit_card",
                "id": "credit_card_6450164",
                "brand": "visa",
                "last_four": "6367"
              },
              "credit_card_6680679": {
                "source": "credit_card",
                "id": "credit_card_6680679",
                "brand": "mastercard",
                "last_four": "5715"
              }
            },
            "orders": [
              "#W2832660",
              "#W1341845",
              "#W3320020"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1341845": {
          "value": {
            "order_id": "#W1341845",
            "user_id": "yara_lee_7701",
            "address": {
              "address1": "490 Highland Drive",
              "address2": "Suite 496",
              "city": "Fort Worth",
              "country": "USA",
              "state": "TX",
              "zip": "76153"
            },
            "items": [
              {
                "name": "LED Light Bulb",
                "product_id": "2696197613",
                "item_id": "6206533187",
                "price": 47.83,
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                }
              },
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "4402162122",
                "price": 233.9,
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                }
              },
              {
                "name": "Bluetooth Speaker",
                "product_id": "4768869376",
                "item_id": "6704763132",
                "price": 305.45,
                "options": {
                  "color": "blue",
                  "battery life": "10 hours",
                  "water resistance": "no"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "712388952344"
                ],
                "item_ids": [
                  "6206533187",
                  "4402162122",
                  "6704763132"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 587.18,
                "payment_method_id": "credit_card_6450164"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "6206533187",
            "4402162122"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "credit_card_6450164",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:yara_lee_7701"
          ],
          "sources": [
            0
          ]
        },
        "requirement:6206533187": {
          "value": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "Bluetooth"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:4402162122": {
          "value": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:2696197613": {
          "value": {
            "name": "LED Light Bulb",
            "product_id": "2696197613",
            "variants": {
              "7445824652": {
                "item_id": "7445824652",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Wi-Fi"
                },
                "available": true,
                "price": 49.8
              },
              "3034017579": {
                "item_id": "3034017579",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "Wi-Fi"
                },
                "available": false,
                "price": 49.72
              },
              "5111440845": {
                "item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "available": true,
                "price": 48.55
              },
              "5570660360": {
                "item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "available": false,
                "price": 51.54
              },
              "6206533187": {
                "item_id": "6206533187",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": false,
                "price": 47.83
              },
              "4938013542": {
                "item_id": "4938013542",
                "options": {
                  "brightness": "100W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": true,
                "price": 47.2
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4402162122": {
          "value": [
            "3616838507"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "catalog:1656367028",
            "order:#W1341845"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4402162122": {
          "value": -7.79,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4402162122",
            "catalog:1656367028"
          ],
          "sources": [
            10
          ]
        },
        "match:6206533187": {
          "value": [
            "5111440845"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:6206533187",
            "catalog:2696197613",
            "order:#W1341845"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:6206533187": {
          "value": 0.72,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:6206533187",
            "catalog:2696197613"
          ],
          "sources": [
            17
          ]
        },
        "total": {
          "value": -7.07,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:6206533187",
            "delta:4402162122"
          ],
          "sources": [
            20
          ]
        },
        "confirmation:4402162122": {
          "value": "701719805a088f0b46f7",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "match:4402162122",
            "delta:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:6206533187": {
          "value": "29a1179698ed8e746771",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:6206533187",
            "match:6206533187",
            "delta:6206533187"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "baa7d23a5b7ca58855d8",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:6206533187",
            "confirmation:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "2696197613": 17,
        "1656367028": 10
      },
      "orders": {
        "#W1341845": {
          "order_id": "#W1341845",
          "user_id": "yara_lee_7701",
          "address": {
            "address1": "490 Highland Drive",
            "address2": "Suite 496",
            "city": "Fort Worth",
            "country": "USA",
            "state": "TX",
            "zip": "76153"
          },
          "items": [
            {
              "name": "LED Light Bulb",
              "product_id": "2696197613",
              "item_id": "6206533187",
              "price": 47.83,
              "options": {
                "brightness": "75W equivalent",
                "color temperature": "warm white",
                "connectivity": "none"
              }
            },
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "4402162122",
              "price": 233.9,
              "options": {
                "switch type": "tactile",
                "backlight": "RGB",
                "size": "60%"
              }
            },
            {
              "name": "Bluetooth Speaker",
              "product_id": "4768869376",
              "item_id": "6704763132",
              "price": 305.45,
              "options": {
                "color": "blue",
                "battery life": "10 hours",
                "water resistance": "no"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "712388952344"
              ],
              "item_ids": [
                "6206533187",
                "4402162122",
                "6704763132"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 587.18,
              "payment_method_id": "credit_card_6450164"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "yara_lee_7701": {
          "user_id": "yara_lee_7701",
          "name": {
            "first_name": "Yara",
            "last_name": "Lee"
          },
          "address": {
            "address1": "944 Laurel Lane",
            "address2": "Suite 386",
            "city": "Houston",
            "country": "USA",
            "state": "TX",
            "zip": "77243"
          },
          "email": "yara.lee9368@example.com",
          "payment_methods": {
            "credit_card_6450164": {
              "source": "credit_card",
              "id": "credit_card_6450164",
              "brand": "visa",
              "last_four": "6367"
            },
            "credit_card_6680679": {
              "source": "credit_card",
              "id": "credit_card_6680679",
              "brand": "mastercard",
              "last_four": "5715"
            }
          },
          "orders": [
            "#W2832660",
            "#W1341845",
            "#W3320020"
          ]
        }
      },
      "evidence": {},
      "authenticated": "yara_lee_7701",
      "scope": [
        "6206533187",
        "4402162122"
      ],
      "requirements": {
        "6206533187": {
          "brightness": "60W equivalent",
          "color temperature": "daylight",
          "connectivity": "Bluetooth"
        },
        "4402162122": {
          "switch type": "tactile",
          "backlight": "white",
          "size": "full size"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5570660360",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "new_price": 51.54,
                "old_price": 47.83,
                "difference": 3.71,
                "sources": [
                  8
                ]
              }
            ],
            "difference": -4.08,
            "fingerprint": "baa7d23a5b7ca58855d8",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5570660360"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5111440845",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "new_price": 48.55,
                "old_price": 47.83,
                "difference": 0.72,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -7.07,
            "fingerprint": "e0a00c118f81b5daf923",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5111440845"
              ]
            ]
          },
          "source": 20
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1341845",
      "payment": "credit_card_6450164",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4402162122"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:6206533187"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:6206533187"
          ]
        },
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 20,
          "changed_record_keys": []
        }
      ]
    }
  },
  "after": {
    "targets": {
      "6206533187": "5111440845",
      "4402162122": "3616838507"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1341845",
        "item_ids": [
          "6206533187",
          "4402162122"
        ],
        "new_item_ids": [
          "5111440845",
          "3616838507"
        ],
        "payment_method_id": "credit_card_6450164"
      },
      "rows": [
        {
          "item_id": "4402162122",
          "new_item_id": "3616838507",
          "options": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "new_price": 226.11,
          "old_price": 233.9,
          "difference": -7.79,
          "sources": [
            10
          ]
        },
        {
          "item_id": "6206533187",
          "new_item_id": "5111440845",
          "options": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "Bluetooth"
          },
          "new_price": 48.55,
          "old_price": 47.83,
          "difference": 0.72,
          "sources": [
            17
          ]
        }
      ],
      "difference": -7.07,
      "fingerprint": "e0a00c118f81b5daf923",
      "order_id": "#W1341845",
      "payment_method_id": "credit_card_6450164",
      "pairs": [
        [
          "4402162122",
          "3616838507"
        ],
        [
          "6206533187",
          "5111440845"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1341845",
          "item_ids": [
            "6206533187",
            "4402162122"
          ],
          "new_item_ids": [
            "5570660360",
            "3616838507"
          ],
          "payment_method_id": "credit_card_6450164"
        }
      },
      {
        "kind": "permission",
        "item_id": "6206533187",
        "variant_id": "5111440845",
        "conditional_stock": true,
        "user_ref": 19,
        "quote": "Replace my CURRENT request for original item 6206533187 with SKU 5111440845, if in stock and whole signed difference <= 10000.00."
      },
      {
        "user_ref": 23,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "current_approval",
        "proposal": {
          "order_id": "#W1341845",
          "item_ids": [
            "6206533187",
            "4402162122"
          ],
          "new_item_ids": [
            "5111440845",
            "3616838507"
          ],
          "payment_method_id": "credit_card_6450164"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 17,
      "public_text": "{\"arguments\":{\"product_id\":\"2696197613\"},\"official_result\":{\"name\":\"LED Light Bulb\",\"product_id\":\"2696197613\",\"variants\":{\"3034017579\":{\"available\":false,\"item_id\":\"3034017579\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"Wi-Fi\"},\"price\":49.72},\"4938013542\":{\"available\":true,\"item_id\":\"4938013542\",\"options\":{\"brightness\":\"100W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.2},\"5111440845\":{\"available\":true,\"item_id\":\"5111440845\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Bluetooth\"},\"price\":48.55},\"5570660360\":{\"available\":false,\"item_id\":\"5570660360\",\"options\":{\"brightness\":\"60W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"none\"},\"price\":51.54},\"6206533187\":{\"available\":false,\"item_id\":\"6206533187\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"warm white\",\"connectivity\":\"none\"},\"price\":47.83},\"7445824652\":{\"available\":true,\"item_id\":\"7445824652\",\"options\":{\"brightness\":\"75W equivalent\",\"color temperature\":\"daylight\",\"connectivity\":\"Wi-Fi\"},\"price\":49.8}}},\"official_tool\":\"get_product_details\"}",
      "observed_kind": "inventory_observation",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "yara_lee_7701",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:yara_lee_7701": {
          "value": {
            "user_id": "yara_lee_7701",
            "name": {
              "first_name": "Yara",
              "last_name": "Lee"
            },
            "address": {
              "address1": "944 Laurel Lane",
              "address2": "Suite 386",
              "city": "Houston",
              "country": "USA",
              "state": "TX",
              "zip": "77243"
            },
            "email": "yara.lee9368@example.com",
            "payment_methods": {
              "credit_card_6450164": {
                "source": "credit_card",
                "id": "credit_card_6450164",
                "brand": "visa",
                "last_four": "6367"
              },
              "credit_card_6680679": {
                "source": "credit_card",
                "id": "credit_card_6680679",
                "brand": "mastercard",
                "last_four": "5715"
              }
            },
            "orders": [
              "#W2832660",
              "#W1341845",
              "#W3320020"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1341845": {
          "value": {
            "order_id": "#W1341845",
            "user_id": "yara_lee_7701",
            "address": {
              "address1": "490 Highland Drive",
              "address2": "Suite 496",
              "city": "Fort Worth",
              "country": "USA",
              "state": "TX",
              "zip": "76153"
            },
            "items": [
              {
                "name": "LED Light Bulb",
                "product_id": "2696197613",
                "item_id": "6206533187",
                "price": 47.83,
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                }
              },
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "4402162122",
                "price": 233.9,
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                }
              },
              {
                "name": "Bluetooth Speaker",
                "product_id": "4768869376",
                "item_id": "6704763132",
                "price": 305.45,
                "options": {
                  "color": "blue",
                  "battery life": "10 hours",
                  "water resistance": "no"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "712388952344"
                ],
                "item_ids": [
                  "6206533187",
                  "4402162122",
                  "6704763132"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 587.18,
                "payment_method_id": "credit_card_6450164"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "6206533187",
            "4402162122"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "credit_card_6450164",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:yara_lee_7701"
          ],
          "sources": [
            0
          ]
        },
        "requirement:6206533187": {
          "value": {
            "brightness": "60W equivalent",
            "color temperature": "daylight",
            "connectivity": "Bluetooth"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            19
          ]
        },
        "requirement:4402162122": {
          "value": {
            "switch type": "tactile",
            "backlight": "white",
            "size": "full size"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:2696197613": {
          "value": {
            "name": "LED Light Bulb",
            "product_id": "2696197613",
            "variants": {
              "7445824652": {
                "item_id": "7445824652",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Wi-Fi"
                },
                "available": true,
                "price": 49.8
              },
              "3034017579": {
                "item_id": "3034017579",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "Wi-Fi"
                },
                "available": false,
                "price": 49.72
              },
              "5111440845": {
                "item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "available": true,
                "price": 48.55
              },
              "5570660360": {
                "item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "available": false,
                "price": 51.54
              },
              "6206533187": {
                "item_id": "6206533187",
                "options": {
                  "brightness": "75W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": false,
                "price": 47.83
              },
              "4938013542": {
                "item_id": "4938013542",
                "options": {
                  "brightness": "100W equivalent",
                  "color temperature": "warm white",
                  "connectivity": "none"
                },
                "available": true,
                "price": 47.2
              }
            }
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            17
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4402162122": {
          "value": [
            "3616838507"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "catalog:1656367028",
            "order:#W1341845"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4402162122": {
          "value": -7.79,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4402162122",
            "catalog:1656367028"
          ],
          "sources": [
            10
          ]
        },
        "match:6206533187": {
          "value": [
            "5111440845"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:6206533187",
            "catalog:2696197613",
            "order:#W1341845"
          ],
          "sources": [
            17,
            19
          ]
        },
        "delta:6206533187": {
          "value": 0.72,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:6206533187",
            "catalog:2696197613"
          ],
          "sources": [
            17
          ]
        },
        "total": {
          "value": -7.07,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:6206533187",
            "delta:4402162122"
          ],
          "sources": [
            20
          ]
        },
        "confirmation:4402162122": {
          "value": "701719805a088f0b46f7",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4402162122",
            "match:4402162122",
            "delta:4402162122"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:6206533187": {
          "value": "80fcedcf32e299e728de",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:6206533187",
            "match:6206533187",
            "delta:6206533187"
          ],
          "sources": [
            22,
            23
          ]
        },
        "authorization": {
          "value": "e0a00c118f81b5daf923",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:6206533187",
            "confirmation:4402162122"
          ],
          "sources": [
            22,
            23
          ]
        }
      },
      "product_refs": {
        "2696197613": 17,
        "1656367028": 10
      },
      "orders": {
        "#W1341845": {
          "order_id": "#W1341845",
          "user_id": "yara_lee_7701",
          "address": {
            "address1": "490 Highland Drive",
            "address2": "Suite 496",
            "city": "Fort Worth",
            "country": "USA",
            "state": "TX",
            "zip": "76153"
          },
          "items": [
            {
              "name": "LED Light Bulb",
              "product_id": "2696197613",
              "item_id": "6206533187",
              "price": 47.83,
              "options": {
                "brightness": "75W equivalent",
                "color temperature": "warm white",
                "connectivity": "none"
              }
            },
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "4402162122",
              "price": 233.9,
              "options": {
                "switch type": "tactile",
                "backlight": "RGB",
                "size": "60%"
              }
            },
            {
              "name": "Bluetooth Speaker",
              "product_id": "4768869376",
              "item_id": "6704763132",
              "price": 305.45,
              "options": {
                "color": "blue",
                "battery life": "10 hours",
                "water resistance": "no"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "712388952344"
              ],
              "item_ids": [
                "6206533187",
                "4402162122",
                "6704763132"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 587.18,
              "payment_method_id": "credit_card_6450164"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "yara_lee_7701": {
          "user_id": "yara_lee_7701",
          "name": {
            "first_name": "Yara",
            "last_name": "Lee"
          },
          "address": {
            "address1": "944 Laurel Lane",
            "address2": "Suite 386",
            "city": "Houston",
            "country": "USA",
            "state": "TX",
            "zip": "77243"
          },
          "email": "yara.lee9368@example.com",
          "payment_methods": {
            "credit_card_6450164": {
              "source": "credit_card",
              "id": "credit_card_6450164",
              "brand": "visa",
              "last_four": "6367"
            },
            "credit_card_6680679": {
              "source": "credit_card",
              "id": "credit_card_6680679",
              "brand": "mastercard",
              "last_four": "5715"
            }
          },
          "orders": [
            "#W2832660",
            "#W1341845",
            "#W3320020"
          ]
        }
      },
      "evidence": {},
      "authenticated": "yara_lee_7701",
      "scope": [
        "6206533187",
        "4402162122"
      ],
      "requirements": {
        "6206533187": {
          "brightness": "60W equivalent",
          "color temperature": "daylight",
          "connectivity": "Bluetooth"
        },
        "4402162122": {
          "switch type": "tactile",
          "backlight": "white",
          "size": "full size"
        }
      },
      "old_confirmations": [
        {
          "fingerprint": "e0a00c118f81b5daf923",
          "user_ref": 23,
          "assistant_ref": 22,
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5111440845",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "difference": -7.07
        }
      ],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5570660360",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5570660360",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "none"
                },
                "new_price": 51.54,
                "old_price": 47.83,
                "difference": 3.71,
                "sources": [
                  8
                ]
              }
            ],
            "difference": -4.08,
            "fingerprint": "baa7d23a5b7ca58855d8",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5570660360"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5111440845",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "new_price": 48.55,
                "old_price": 47.83,
                "difference": 0.72,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -7.07,
            "fingerprint": "e0a00c118f81b5daf923",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5111440845"
              ]
            ]
          },
          "source": 20
        },
        {
          "arguments": {
            "order_id": "#W1341845",
            "item_ids": [
              "6206533187",
              "4402162122"
            ],
            "new_item_ids": [
              "5111440845",
              "3616838507"
            ],
            "payment_method_id": "credit_card_6450164"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4402162122",
                "new_item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "new_price": 226.11,
                "old_price": 233.9,
                "difference": -7.79,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "6206533187",
                "new_item_id": "5111440845",
                "options": {
                  "brightness": "60W equivalent",
                  "color temperature": "daylight",
                  "connectivity": "Bluetooth"
                },
                "new_price": 48.55,
                "old_price": 47.83,
                "difference": 0.72,
                "sources": [
                  17
                ]
              }
            ],
            "difference": -7.07,
            "fingerprint": "e0a00c118f81b5daf923",
            "order_id": "#W1341845",
            "payment_method_id": "credit_card_6450164",
            "pairs": [
              [
                "4402162122",
                "3616838507"
              ],
              [
                "6206533187",
                "5111440845"
              ]
            ]
          },
          "source": 22
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1341845",
      "payment": "credit_card_6450164",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4402162122"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:6206533187"
          ]
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 19,
          "changed_record_keys": [
            "match:6206533187"
          ]
        },
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 20,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4402162122"
          ],
          "source": 22,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "6206533187"
          ],
          "source": 22,
          "changed_record_keys": []
        }
      ]
    }
  }
}
```
首个后续工作：`{"event":6,"object":"6206533187","parameters":{"variant_id":"5111440845"},"reason":"Current requested SKU 5570660360 is out of stock; no exact match exists. Variant 5111440845 is available within cap and matches brightness and color temperature, differing only in connectivity, so it is the closest negotiable alternative requiring new user permission.","source":"decision_model","work_type":"clarify"}`

## A_E_EDB07_r1_framework

```json
{
  "event": 4,
  "module": "public_change",
  "change": null,
  "model_update": null,
  "before": {},
  "after": {}
}
```
```json
{
  "event": 5,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 14
      },
      {
        "kind": "permission",
        "source_ref": 16,
        "quote": "change ONLY original item 9570044148 to SKU 1421289881, if in stock",
        "item_id": "9570044148",
        "variant_id": "1421289881",
        "conditional_stock": true
      }
    ],
    "processed_refs": [
      15,
      16
    ],
    "needs_clarification": false,
    "analysis": "Message 15 approves assistant proposal 14 exactly. Message 16 grants conditional permission to change only item 9570044148 to SKU 1421289881 if in stock, leaves the other item and payment unchanged, and explicitly withdraws prior approval for the new plan, requiring fresh approval."
  },
  "before": {
    "targets": {
      "9570044148": "1151293680",
      "4983901480": "4953074738"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1483350",
        "item_ids": [
          "9570044148",
          "4983901480"
        ],
        "new_item_ids": [
          "1151293680",
          "4953074738"
        ],
        "payment_method_id": "paypal_2319812"
      },
      "rows": [
        {
          "item_id": "4983901480",
          "new_item_id": "4953074738",
          "options": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "new_price": 226.02,
          "old_price": 262.47,
          "difference": -36.45,
          "sources": [
            10
          ]
        },
        {
          "item_id": "9570044148",
          "new_item_id": "1151293680",
          "options": {
            "switch type": "linear",
            "backlight": "RGB",
            "size": "full size"
          },
          "new_price": 272.33,
          "old_price": 231.37,
          "difference": 40.96,
          "sources": [
            8
          ]
        }
      ],
      "difference": 4.51,
      "fingerprint": "36b73193e480e4038297",
      "order_id": "#W1483350",
      "payment_method_id": "paypal_2319812",
      "pairs": [
        [
          "4983901480",
          "4953074738"
        ],
        [
          "9570044148",
          "1151293680"
        ]
      ]
    },
    "pending": [
      15,
      16
    ],
    "parsed_history": [],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 16,
      "public_text": "Before submission, change ONLY original item 9570044148 to SKU 1421289881, if in stock. Other item and original payment stay unchanged. My previous approval does not authorize this new complete plan; ask fresh approval.",
      "observed_kind": "user_message",
      "unparsed_user_change": true
    },
    "core": {
      "records": {
        "identity": {
          "value": "noah_khan_5763",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:noah_khan_5763": {
          "value": {
            "user_id": "noah_khan_5763",
            "name": {
              "first_name": "Noah",
              "last_name": "Khan"
            },
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "email": "noah.khan7453@example.com",
            "payment_methods": {
              "paypal_2319812": {
                "source": "paypal",
                "id": "paypal_2319812"
              }
            },
            "orders": [
              "#W1483350",
              "#W3818056"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1483350": {
          "value": {
            "order_id": "#W1483350",
            "user_id": "noah_khan_5763",
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "items": [
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "9570044148",
                "price": 231.37,
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                }
              },
              {
                "name": "Smart Thermostat",
                "product_id": "4896585277",
                "item_id": "4983901480",
                "price": 262.47,
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                }
              },
              {
                "name": "Digital Camera",
                "product_id": "8940227892",
                "item_id": "4326528037",
                "price": 2714.51,
                "options": {
                  "resolution": "24MP",
                  "zoom": "5x",
                  "storage": "CF card"
                }
              },
              {
                "name": "Cycling Helmet",
                "product_id": "7765186836",
                "item_id": "6697922351",
                "price": 194.47,
                "options": {
                  "size": "L",
                  "color": "white",
                  "ventilation": "medium"
                }
              },
              {
                "name": "Smart Watch",
                "product_id": "6945232052",
                "item_id": "9320099340",
                "price": 375.03,
                "options": {
                  "color": "black",
                  "band material": "leather",
                  "display": "AMOLED"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "151624030573"
                ],
                "item_ids": [
                  "9570044148",
                  "4983901480",
                  "4326528037",
                  "6697922351",
                  "9320099340"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3777.85,
                "payment_method_id": "paypal_2319812"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "9570044148",
            "4983901480"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_2319812",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:noah_khan_5763"
          ],
          "sources": [
            0
          ]
        },
        "requirement:9570044148": {
          "value": {
            "switch type": "linear",
            "backlight": "RGB",
            "size": "full size"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "requirement:4983901480": {
          "value": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            8
          ]
        },
        "catalog:4896585277": {
          "value": {
            "name": "Smart Thermostat",
            "product_id": "4896585277",
            "variants": {
              "8722653925": {
                "item_id": "8722653925",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "white"
                },
                "available": false,
                "price": 227.8
              },
              "8593894906": {
                "item_id": "8593894906",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "white"
                },
                "available": false,
                "price": 263.11
              },
              "2791467853": {
                "item_id": "2791467853",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "stainless steel"
                },
                "available": false,
                "price": 242.53
              },
              "7747408585": {
                "item_id": "7747408585",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "black"
                },
                "available": true,
                "price": 249.01
              },
              "4953074738": {
                "item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "available": true,
                "price": 226.02
              },
              "4983901480": {
                "item_id": "4983901480",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                },
                "available": true,
                "price": 262.47
              },
              "9480266227": {
                "item_id": "9480266227",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 255.98
              },
              "6243148452": {
                "item_id": "6243148452",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 247.0
              },
              "3377900078": {
                "item_id": "3377900078",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "white"
                },
                "available": true,
                "price": 260.68
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4983901480": {
          "value": [
            "4953074738"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4983901480",
            "catalog:4896585277",
            "order:#W1483350"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4983901480": {
          "value": -36.45,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4983901480",
            "catalog:4896585277"
          ],
          "sources": [
            10
          ]
        },
        "match:9570044148": {
          "value": [
            "1151293680"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:9570044148",
            "catalog:1656367028",
            "order:#W1483350"
          ],
          "sources": [
            8,
            12
          ]
        },
        "delta:9570044148": {
          "value": 40.96,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:9570044148",
            "catalog:1656367028"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 4.51,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "delta:9570044148",
            "delta:4983901480"
          ],
          "sources": [
            12
          ]
        }
      },
      "product_refs": {
        "1656367028": 8,
        "4896585277": 10
      },
      "orders": {
        "#W1483350": {
          "order_id": "#W1483350",
          "user_id": "noah_khan_5763",
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "items": [
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "9570044148",
              "price": 231.37,
              "options": {
                "switch type": "linear",
                "backlight": "none",
                "size": "full size"
              }
            },
            {
              "name": "Smart Thermostat",
              "product_id": "4896585277",
              "item_id": "4983901480",
              "price": 262.47,
              "options": {
                "compatibility": "Apple HomeKit",
                "color": "black"
              }
            },
            {
              "name": "Digital Camera",
              "product_id": "8940227892",
              "item_id": "4326528037",
              "price": 2714.51,
              "options": {
                "resolution": "24MP",
                "zoom": "5x",
                "storage": "CF card"
              }
            },
            {
              "name": "Cycling Helmet",
              "product_id": "7765186836",
              "item_id": "6697922351",
              "price": 194.47,
              "options": {
                "size": "L",
                "color": "white",
                "ventilation": "medium"
              }
            },
            {
              "name": "Smart Watch",
              "product_id": "6945232052",
              "item_id": "9320099340",
              "price": 375.03,
              "options": {
                "color": "black",
                "band material": "leather",
                "display": "AMOLED"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "151624030573"
              ],
              "item_ids": [
                "9570044148",
                "4983901480",
                "4326528037",
                "6697922351",
                "9320099340"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3777.85,
              "payment_method_id": "paypal_2319812"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "noah_khan_5763": {
          "user_id": "noah_khan_5763",
          "name": {
            "first_name": "Noah",
            "last_name": "Khan"
          },
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "email": "noah.khan7453@example.com",
          "payment_methods": {
            "paypal_2319812": {
              "source": "paypal",
              "id": "paypal_2319812"
            }
          },
          "orders": [
            "#W1483350",
            "#W3818056"
          ]
        }
      },
      "evidence": {},
      "authenticated": "noah_khan_5763",
      "scope": [
        "9570044148",
        "4983901480"
      ],
      "requirements": {
        "9570044148": {
          "switch type": "linear",
          "backlight": "RGB",
          "size": "full size"
        },
        "4983901480": {
          "compatibility": "Amazon Alexa",
          "color": "black"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1151293680",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4983901480",
                "new_item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "new_price": 226.02,
                "old_price": 262.47,
                "difference": -36.45,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "9570044148",
                "new_item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "new_price": 272.33,
                "old_price": 231.37,
                "difference": 40.96,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 4.51,
            "fingerprint": "36b73193e480e4038297",
            "order_id": "#W1483350",
            "payment_method_id": "paypal_2319812",
            "pairs": [
              [
                "4983901480",
                "4953074738"
              ],
              [
                "9570044148",
                "1151293680"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1483350",
      "payment": "paypal_2319812",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4983901480"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4983901480"
          ]
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:9570044148"
          ]
        }
      ]
    }
  },
  "after": {
    "targets": {
      "9570044148": "1421289881",
      "4983901480": "4953074738"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1483350",
        "item_ids": [
          "9570044148",
          "4983901480"
        ],
        "new_item_ids": [
          "1151293680",
          "4953074738"
        ],
        "payment_method_id": "paypal_2319812"
      },
      "rows": [
        {
          "item_id": "4983901480",
          "new_item_id": "4953074738",
          "options": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "new_price": 226.02,
          "old_price": 262.47,
          "difference": -36.45,
          "sources": [
            10
          ]
        },
        {
          "item_id": "9570044148",
          "new_item_id": "1151293680",
          "options": {
            "switch type": "linear",
            "backlight": "RGB",
            "size": "full size"
          },
          "new_price": 272.33,
          "old_price": 231.37,
          "difference": 40.96,
          "sources": [
            8
          ]
        }
      ],
      "difference": 4.51,
      "fingerprint": "36b73193e480e4038297",
      "order_id": "#W1483350",
      "payment_method_id": "paypal_2319812",
      "pairs": [
        [
          "4983901480",
          "4953074738"
        ],
        [
          "9570044148",
          "1151293680"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "kind": "permission",
        "item_id": "9570044148",
        "variant_id": "1421289881",
        "conditional_stock": true,
        "user_ref": 16,
        "quote": "change ONLY original item 9570044148 to SKU 1421289881, if in stock"
      },
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1483350",
          "item_ids": [
            "9570044148",
            "4983901480"
          ],
          "new_item_ids": [
            "1151293680",
            "4953074738"
          ],
          "payment_method_id": "paypal_2319812"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 16,
      "public_text": "Before submission, change ONLY original item 9570044148 to SKU 1421289881, if in stock. Other item and original payment stay unchanged. My previous approval does not authorize this new complete plan; ask fresh approval.",
      "observed_kind": "user_message",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "noah_khan_5763",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:noah_khan_5763": {
          "value": {
            "user_id": "noah_khan_5763",
            "name": {
              "first_name": "Noah",
              "last_name": "Khan"
            },
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "email": "noah.khan7453@example.com",
            "payment_methods": {
              "paypal_2319812": {
                "source": "paypal",
                "id": "paypal_2319812"
              }
            },
            "orders": [
              "#W1483350",
              "#W3818056"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1483350": {
          "value": {
            "order_id": "#W1483350",
            "user_id": "noah_khan_5763",
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "items": [
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "9570044148",
                "price": 231.37,
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                }
              },
              {
                "name": "Smart Thermostat",
                "product_id": "4896585277",
                "item_id": "4983901480",
                "price": 262.47,
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                }
              },
              {
                "name": "Digital Camera",
                "product_id": "8940227892",
                "item_id": "4326528037",
                "price": 2714.51,
                "options": {
                  "resolution": "24MP",
                  "zoom": "5x",
                  "storage": "CF card"
                }
              },
              {
                "name": "Cycling Helmet",
                "product_id": "7765186836",
                "item_id": "6697922351",
                "price": 194.47,
                "options": {
                  "size": "L",
                  "color": "white",
                  "ventilation": "medium"
                }
              },
              {
                "name": "Smart Watch",
                "product_id": "6945232052",
                "item_id": "9320099340",
                "price": 375.03,
                "options": {
                  "color": "black",
                  "band material": "leather",
                  "display": "AMOLED"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "151624030573"
                ],
                "item_ids": [
                  "9570044148",
                  "4983901480",
                  "4326528037",
                  "6697922351",
                  "9320099340"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3777.85,
                "payment_method_id": "paypal_2319812"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "9570044148",
            "4983901480"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_2319812",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:noah_khan_5763"
          ],
          "sources": [
            0
          ]
        },
        "requirement:9570044148": {
          "value": {
            "switch type": "linear",
            "backlight": "none",
            "size": "80%"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            16
          ]
        },
        "requirement:4983901480": {
          "value": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            8
          ]
        },
        "catalog:4896585277": {
          "value": {
            "name": "Smart Thermostat",
            "product_id": "4896585277",
            "variants": {
              "8722653925": {
                "item_id": "8722653925",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "white"
                },
                "available": false,
                "price": 227.8
              },
              "8593894906": {
                "item_id": "8593894906",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "white"
                },
                "available": false,
                "price": 263.11
              },
              "2791467853": {
                "item_id": "2791467853",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "stainless steel"
                },
                "available": false,
                "price": 242.53
              },
              "7747408585": {
                "item_id": "7747408585",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "black"
                },
                "available": true,
                "price": 249.01
              },
              "4953074738": {
                "item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "available": true,
                "price": 226.02
              },
              "4983901480": {
                "item_id": "4983901480",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                },
                "available": true,
                "price": 262.47
              },
              "9480266227": {
                "item_id": "9480266227",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 255.98
              },
              "6243148452": {
                "item_id": "6243148452",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 247.0
              },
              "3377900078": {
                "item_id": "3377900078",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "white"
                },
                "available": true,
                "price": 260.68
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4983901480": {
          "value": [
            "4953074738"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4983901480",
            "catalog:4896585277",
            "order:#W1483350"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4983901480": {
          "value": -36.45,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4983901480",
            "catalog:4896585277"
          ],
          "sources": [
            10
          ]
        },
        "match:9570044148": {
          "value": [
            "1421289881"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:9570044148",
            "catalog:1656367028",
            "order:#W1483350"
          ],
          "sources": [
            8,
            16
          ]
        },
        "delta:9570044148": {
          "value": 40.96,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "match:9570044148",
            "catalog:1656367028"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 4.51,
          "version": 1,
          "status": "stale",
          "depends_on": [
            "delta:9570044148",
            "delta:4983901480"
          ],
          "sources": [
            12
          ]
        },
        "confirmation:4983901480": {
          "value": "3ba8b2d04fbd21b430ac",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4983901480",
            "match:4983901480",
            "delta:4983901480"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:9570044148": {
          "value": "8f0b5814766d742a4fbf",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:9570044148",
            "match:9570044148",
            "delta:9570044148"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "36b73193e480e4038297",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:9570044148",
            "confirmation:4983901480"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "1656367028": 8,
        "4896585277": 10
      },
      "orders": {
        "#W1483350": {
          "order_id": "#W1483350",
          "user_id": "noah_khan_5763",
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "items": [
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "9570044148",
              "price": 231.37,
              "options": {
                "switch type": "linear",
                "backlight": "none",
                "size": "full size"
              }
            },
            {
              "name": "Smart Thermostat",
              "product_id": "4896585277",
              "item_id": "4983901480",
              "price": 262.47,
              "options": {
                "compatibility": "Apple HomeKit",
                "color": "black"
              }
            },
            {
              "name": "Digital Camera",
              "product_id": "8940227892",
              "item_id": "4326528037",
              "price": 2714.51,
              "options": {
                "resolution": "24MP",
                "zoom": "5x",
                "storage": "CF card"
              }
            },
            {
              "name": "Cycling Helmet",
              "product_id": "7765186836",
              "item_id": "6697922351",
              "price": 194.47,
              "options": {
                "size": "L",
                "color": "white",
                "ventilation": "medium"
              }
            },
            {
              "name": "Smart Watch",
              "product_id": "6945232052",
              "item_id": "9320099340",
              "price": 375.03,
              "options": {
                "color": "black",
                "band material": "leather",
                "display": "AMOLED"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "151624030573"
              ],
              "item_ids": [
                "9570044148",
                "4983901480",
                "4326528037",
                "6697922351",
                "9320099340"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3777.85,
              "payment_method_id": "paypal_2319812"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "noah_khan_5763": {
          "user_id": "noah_khan_5763",
          "name": {
            "first_name": "Noah",
            "last_name": "Khan"
          },
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "email": "noah.khan7453@example.com",
          "payment_methods": {
            "paypal_2319812": {
              "source": "paypal",
              "id": "paypal_2319812"
            }
          },
          "orders": [
            "#W1483350",
            "#W3818056"
          ]
        }
      },
      "evidence": {},
      "authenticated": "noah_khan_5763",
      "scope": [
        "9570044148",
        "4983901480"
      ],
      "requirements": {
        "9570044148": {
          "switch type": "linear",
          "backlight": "none",
          "size": "80%"
        },
        "4983901480": {
          "compatibility": "Amazon Alexa",
          "color": "black"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1151293680",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4983901480",
                "new_item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "new_price": 226.02,
                "old_price": 262.47,
                "difference": -36.45,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "9570044148",
                "new_item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "new_price": 272.33,
                "old_price": 231.37,
                "difference": 40.96,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 4.51,
            "fingerprint": "36b73193e480e4038297",
            "order_id": "#W1483350",
            "payment_method_id": "paypal_2319812",
            "pairs": [
              [
                "4983901480",
                "4953074738"
              ],
              [
                "9570044148",
                "1151293680"
              ]
            ]
          },
          "source": 12
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1483350",
      "payment": "paypal_2319812",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4983901480"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4983901480"
          ]
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:9570044148"
          ]
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 16,
          "changed_record_keys": [
            "match:9570044148"
          ]
        }
      ]
    }
  }
}
```
```json
{
  "event": 10,
  "module": "semantic_update",
  "change": null,
  "model_update": {
    "updates": [
      {
        "kind": "approval",
        "source_ref": 20,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "proposal_ref": 19
      }
    ],
    "processed_refs": [
      20
    ],
    "needs_clarification": false,
    "analysis": "User explicitly approves the complete combined proposal referenced by assistant_ref 19."
  },
  "before": {
    "targets": {
      "9570044148": "1421289881",
      "4983901480": "4953074738"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1483350",
        "item_ids": [
          "9570044148",
          "4983901480"
        ],
        "new_item_ids": [
          "1421289881",
          "4953074738"
        ],
        "payment_method_id": "paypal_2319812"
      },
      "rows": [
        {
          "item_id": "4983901480",
          "new_item_id": "4953074738",
          "options": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "new_price": 226.02,
          "old_price": 262.47,
          "difference": -36.45,
          "sources": [
            10
          ]
        },
        {
          "item_id": "9570044148",
          "new_item_id": "1421289881",
          "options": {
            "switch type": "linear",
            "backlight": "none",
            "size": "80%"
          },
          "new_price": 268.77,
          "old_price": 231.37,
          "difference": 37.4,
          "sources": [
            8
          ]
        }
      ],
      "difference": 0.95,
      "fingerprint": "1aeb3d51ffd6200fc779",
      "order_id": "#W1483350",
      "payment_method_id": "paypal_2319812",
      "pairs": [
        [
          "4983901480",
          "4953074738"
        ],
        [
          "9570044148",
          "1421289881"
        ]
      ]
    },
    "pending": [
      20
    ],
    "parsed_history": [
      {
        "kind": "permission",
        "item_id": "9570044148",
        "variant_id": "1421289881",
        "conditional_stock": true,
        "user_ref": 16,
        "quote": "change ONLY original item 9570044148 to SKU 1421289881, if in stock"
      },
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1483350",
          "item_ids": [
            "9570044148",
            "4983901480"
          ],
          "new_item_ids": [
            "1151293680",
            "4953074738"
          ],
          "payment_method_id": "paypal_2319812"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 16,
      "public_text": "Before submission, change ONLY original item 9570044148 to SKU 1421289881, if in stock. Other item and original payment stay unchanged. My previous approval does not authorize this new complete plan; ask fresh approval.",
      "observed_kind": "user_message",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "noah_khan_5763",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:noah_khan_5763": {
          "value": {
            "user_id": "noah_khan_5763",
            "name": {
              "first_name": "Noah",
              "last_name": "Khan"
            },
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "email": "noah.khan7453@example.com",
            "payment_methods": {
              "paypal_2319812": {
                "source": "paypal",
                "id": "paypal_2319812"
              }
            },
            "orders": [
              "#W1483350",
              "#W3818056"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1483350": {
          "value": {
            "order_id": "#W1483350",
            "user_id": "noah_khan_5763",
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "items": [
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "9570044148",
                "price": 231.37,
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                }
              },
              {
                "name": "Smart Thermostat",
                "product_id": "4896585277",
                "item_id": "4983901480",
                "price": 262.47,
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                }
              },
              {
                "name": "Digital Camera",
                "product_id": "8940227892",
                "item_id": "4326528037",
                "price": 2714.51,
                "options": {
                  "resolution": "24MP",
                  "zoom": "5x",
                  "storage": "CF card"
                }
              },
              {
                "name": "Cycling Helmet",
                "product_id": "7765186836",
                "item_id": "6697922351",
                "price": 194.47,
                "options": {
                  "size": "L",
                  "color": "white",
                  "ventilation": "medium"
                }
              },
              {
                "name": "Smart Watch",
                "product_id": "6945232052",
                "item_id": "9320099340",
                "price": 375.03,
                "options": {
                  "color": "black",
                  "band material": "leather",
                  "display": "AMOLED"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "151624030573"
                ],
                "item_ids": [
                  "9570044148",
                  "4983901480",
                  "4326528037",
                  "6697922351",
                  "9320099340"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3777.85,
                "payment_method_id": "paypal_2319812"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "9570044148",
            "4983901480"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_2319812",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:noah_khan_5763"
          ],
          "sources": [
            0
          ]
        },
        "requirement:9570044148": {
          "value": {
            "switch type": "linear",
            "backlight": "none",
            "size": "80%"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            16
          ]
        },
        "requirement:4983901480": {
          "value": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            8
          ]
        },
        "catalog:4896585277": {
          "value": {
            "name": "Smart Thermostat",
            "product_id": "4896585277",
            "variants": {
              "8722653925": {
                "item_id": "8722653925",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "white"
                },
                "available": false,
                "price": 227.8
              },
              "8593894906": {
                "item_id": "8593894906",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "white"
                },
                "available": false,
                "price": 263.11
              },
              "2791467853": {
                "item_id": "2791467853",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "stainless steel"
                },
                "available": false,
                "price": 242.53
              },
              "7747408585": {
                "item_id": "7747408585",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "black"
                },
                "available": true,
                "price": 249.01
              },
              "4953074738": {
                "item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "available": true,
                "price": 226.02
              },
              "4983901480": {
                "item_id": "4983901480",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                },
                "available": true,
                "price": 262.47
              },
              "9480266227": {
                "item_id": "9480266227",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 255.98
              },
              "6243148452": {
                "item_id": "6243148452",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 247.0
              },
              "3377900078": {
                "item_id": "3377900078",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "white"
                },
                "available": true,
                "price": 260.68
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4983901480": {
          "value": [
            "4953074738"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4983901480",
            "catalog:4896585277",
            "order:#W1483350"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4983901480": {
          "value": -36.45,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4983901480",
            "catalog:4896585277"
          ],
          "sources": [
            10
          ]
        },
        "match:9570044148": {
          "value": [
            "1421289881"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:9570044148",
            "catalog:1656367028",
            "order:#W1483350"
          ],
          "sources": [
            8,
            16
          ]
        },
        "delta:9570044148": {
          "value": 37.4,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:9570044148",
            "catalog:1656367028"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 0.95,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:9570044148",
            "delta:4983901480"
          ],
          "sources": [
            17
          ]
        },
        "confirmation:4983901480": {
          "value": "3ba8b2d04fbd21b430ac",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4983901480",
            "match:4983901480",
            "delta:4983901480"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:9570044148": {
          "value": "8f0b5814766d742a4fbf",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "requirement:9570044148",
            "match:9570044148",
            "delta:9570044148"
          ],
          "sources": [
            14,
            15
          ]
        },
        "authorization": {
          "value": "36b73193e480e4038297",
          "version": 1,
          "status": "stale",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:9570044148",
            "confirmation:4983901480"
          ],
          "sources": [
            14,
            15
          ]
        }
      },
      "product_refs": {
        "1656367028": 8,
        "4896585277": 10
      },
      "orders": {
        "#W1483350": {
          "order_id": "#W1483350",
          "user_id": "noah_khan_5763",
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "items": [
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "9570044148",
              "price": 231.37,
              "options": {
                "switch type": "linear",
                "backlight": "none",
                "size": "full size"
              }
            },
            {
              "name": "Smart Thermostat",
              "product_id": "4896585277",
              "item_id": "4983901480",
              "price": 262.47,
              "options": {
                "compatibility": "Apple HomeKit",
                "color": "black"
              }
            },
            {
              "name": "Digital Camera",
              "product_id": "8940227892",
              "item_id": "4326528037",
              "price": 2714.51,
              "options": {
                "resolution": "24MP",
                "zoom": "5x",
                "storage": "CF card"
              }
            },
            {
              "name": "Cycling Helmet",
              "product_id": "7765186836",
              "item_id": "6697922351",
              "price": 194.47,
              "options": {
                "size": "L",
                "color": "white",
                "ventilation": "medium"
              }
            },
            {
              "name": "Smart Watch",
              "product_id": "6945232052",
              "item_id": "9320099340",
              "price": 375.03,
              "options": {
                "color": "black",
                "band material": "leather",
                "display": "AMOLED"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "151624030573"
              ],
              "item_ids": [
                "9570044148",
                "4983901480",
                "4326528037",
                "6697922351",
                "9320099340"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3777.85,
              "payment_method_id": "paypal_2319812"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "noah_khan_5763": {
          "user_id": "noah_khan_5763",
          "name": {
            "first_name": "Noah",
            "last_name": "Khan"
          },
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "email": "noah.khan7453@example.com",
          "payment_methods": {
            "paypal_2319812": {
              "source": "paypal",
              "id": "paypal_2319812"
            }
          },
          "orders": [
            "#W1483350",
            "#W3818056"
          ]
        }
      },
      "evidence": {},
      "authenticated": "noah_khan_5763",
      "scope": [
        "9570044148",
        "4983901480"
      ],
      "requirements": {
        "9570044148": {
          "switch type": "linear",
          "backlight": "none",
          "size": "80%"
        },
        "4983901480": {
          "compatibility": "Amazon Alexa",
          "color": "black"
        }
      },
      "old_confirmations": [],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1151293680",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4983901480",
                "new_item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "new_price": 226.02,
                "old_price": 262.47,
                "difference": -36.45,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "9570044148",
                "new_item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "new_price": 272.33,
                "old_price": 231.37,
                "difference": 40.96,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 4.51,
            "fingerprint": "36b73193e480e4038297",
            "order_id": "#W1483350",
            "payment_method_id": "paypal_2319812",
            "pairs": [
              [
                "4983901480",
                "4953074738"
              ],
              [
                "9570044148",
                "1151293680"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1421289881",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4983901480",
                "new_item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "new_price": 226.02,
                "old_price": 262.47,
                "difference": -36.45,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "9570044148",
                "new_item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "new_price": 268.77,
                "old_price": 231.37,
                "difference": 37.4,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 0.95,
            "fingerprint": "1aeb3d51ffd6200fc779",
            "order_id": "#W1483350",
            "payment_method_id": "paypal_2319812",
            "pairs": [
              [
                "4983901480",
                "4953074738"
              ],
              [
                "9570044148",
                "1421289881"
              ]
            ]
          },
          "source": 17
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1483350",
      "payment": "paypal_2319812",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4983901480"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4983901480"
          ]
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:9570044148"
          ]
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 16,
          "changed_record_keys": [
            "match:9570044148"
          ]
        },
        {
          "item_ids": [
            "4983901480"
          ],
          "source": 17,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 17,
          "changed_record_keys": []
        }
      ]
    }
  },
  "after": {
    "targets": {
      "9570044148": "1421289881",
      "4983901480": "4953074738"
    },
    "hard_cap": "10000.00",
    "plan": {
      "arguments": {
        "order_id": "#W1483350",
        "item_ids": [
          "9570044148",
          "4983901480"
        ],
        "new_item_ids": [
          "1421289881",
          "4953074738"
        ],
        "payment_method_id": "paypal_2319812"
      },
      "rows": [
        {
          "item_id": "4983901480",
          "new_item_id": "4953074738",
          "options": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "new_price": 226.02,
          "old_price": 262.47,
          "difference": -36.45,
          "sources": [
            10
          ]
        },
        {
          "item_id": "9570044148",
          "new_item_id": "1421289881",
          "options": {
            "switch type": "linear",
            "backlight": "none",
            "size": "80%"
          },
          "new_price": 268.77,
          "old_price": 231.37,
          "difference": 37.4,
          "sources": [
            8
          ]
        }
      ],
      "difference": 0.95,
      "fingerprint": "1aeb3d51ffd6200fc779",
      "order_id": "#W1483350",
      "payment_method_id": "paypal_2319812",
      "pairs": [
        [
          "4983901480",
          "4953074738"
        ],
        [
          "9570044148",
          "1421289881"
        ]
      ]
    },
    "pending": [],
    "parsed_history": [
      {
        "kind": "permission",
        "item_id": "9570044148",
        "variant_id": "1421289881",
        "conditional_stock": true,
        "user_ref": 16,
        "quote": "change ONLY original item 9570044148 to SKU 1421289881, if in stock"
      },
      {
        "user_ref": 15,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "historical_approval",
        "proposal": {
          "order_id": "#W1483350",
          "item_ids": [
            "9570044148",
            "4983901480"
          ],
          "new_item_ids": [
            "1151293680",
            "4953074738"
          ],
          "payment_method_id": "paypal_2319812"
        }
      },
      {
        "user_ref": 20,
        "quote": "Yes, I approve exactly that complete current exchange proposal, all listed items, stated exact amount and refund/payment method.",
        "kind": "current_approval",
        "proposal": {
          "order_id": "#W1483350",
          "item_ids": [
            "9570044148",
            "4983901480"
          ],
          "new_item_ids": [
            "1421289881",
            "4953074738"
          ],
          "payment_method_id": "paypal_2319812"
        }
      }
    ],
    "withdrawn": false,
    "stopped": false,
    "change": {
      "source_ref": 16,
      "public_text": "Before submission, change ONLY original item 9570044148 to SKU 1421289881, if in stock. Other item and original payment stay unchanged. My previous approval does not authorize this new complete plan; ask fresh approval.",
      "observed_kind": "user_message",
      "unparsed_user_change": false
    },
    "core": {
      "records": {
        "identity": {
          "value": "noah_khan_5763",
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            2
          ]
        },
        "profile:noah_khan_5763": {
          "value": {
            "user_id": "noah_khan_5763",
            "name": {
              "first_name": "Noah",
              "last_name": "Khan"
            },
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "email": "noah.khan7453@example.com",
            "payment_methods": {
              "paypal_2319812": {
                "source": "paypal",
                "id": "paypal_2319812"
              }
            },
            "orders": [
              "#W1483350",
              "#W3818056"
            ]
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            4
          ]
        },
        "order:#W1483350": {
          "value": {
            "order_id": "#W1483350",
            "user_id": "noah_khan_5763",
            "address": {
              "address1": "143 Highland Drive",
              "address2": "Suite 928",
              "city": "San Francisco",
              "country": "USA",
              "state": "CA",
              "zip": "94140"
            },
            "items": [
              {
                "name": "Mechanical Keyboard",
                "product_id": "1656367028",
                "item_id": "9570044148",
                "price": 231.37,
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                }
              },
              {
                "name": "Smart Thermostat",
                "product_id": "4896585277",
                "item_id": "4983901480",
                "price": 262.47,
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                }
              },
              {
                "name": "Digital Camera",
                "product_id": "8940227892",
                "item_id": "4326528037",
                "price": 2714.51,
                "options": {
                  "resolution": "24MP",
                  "zoom": "5x",
                  "storage": "CF card"
                }
              },
              {
                "name": "Cycling Helmet",
                "product_id": "7765186836",
                "item_id": "6697922351",
                "price": 194.47,
                "options": {
                  "size": "L",
                  "color": "white",
                  "ventilation": "medium"
                }
              },
              {
                "name": "Smart Watch",
                "product_id": "6945232052",
                "item_id": "9320099340",
                "price": 375.03,
                "options": {
                  "color": "black",
                  "band material": "leather",
                  "display": "AMOLED"
                }
              }
            ],
            "status": "delivered",
            "fulfillments": [
              {
                "tracking_id": [
                  "151624030573"
                ],
                "item_ids": [
                  "9570044148",
                  "4983901480",
                  "4326528037",
                  "6697922351",
                  "9320099340"
                ]
              }
            ],
            "payment_history": [
              {
                "transaction_type": "payment",
                "amount": 3777.85,
                "payment_method_id": "paypal_2319812"
              }
            ],
            "cancel_reason": null,
            "exchange_items": null,
            "exchange_new_items": null,
            "exchange_payment_method_id": null,
            "exchange_price_difference": null,
            "return_items": null,
            "return_payment_method_id": null
          },
          "version": 1,
          "status": "supported",
          "depends_on": [
            "identity"
          ],
          "sources": [
            6
          ]
        },
        "scope": {
          "value": [
            "9570044148",
            "4983901480"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "payment": {
          "value": "paypal_2319812",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "profile:noah_khan_5763"
          ],
          "sources": [
            0
          ]
        },
        "requirement:9570044148": {
          "value": {
            "switch type": "linear",
            "backlight": "none",
            "size": "80%"
          },
          "version": 2,
          "status": "supported",
          "depends_on": [],
          "sources": [
            16
          ]
        },
        "requirement:4983901480": {
          "value": {
            "compatibility": "Amazon Alexa",
            "color": "black"
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            0
          ]
        },
        "catalog:1656367028": {
          "value": {
            "name": "Mechanical Keyboard",
            "product_id": "1656367028",
            "variants": {
              "9690244451": {
                "item_id": "9690244451",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": false,
                "price": 236.51
              },
              "7706410293": {
                "item_id": "7706410293",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 269.16
              },
              "3616838507": {
                "item_id": "3616838507",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 226.11
              },
              "8484921793": {
                "item_id": "8484921793",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 230.15
              },
              "1340995114": {
                "item_id": "1340995114",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": false,
                "price": 235.13
              },
              "6342039236": {
                "item_id": "6342039236",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": true,
                "price": 244.91
              },
              "1421289881": {
                "item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 268.77
              },
              "7867398203": {
                "item_id": "7867398203",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 232.7
              },
              "4648814700": {
                "item_id": "4648814700",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "60%"
                },
                "available": false,
                "price": 228.84
              },
              "5222576926": {
                "item_id": "5222576926",
                "options": {
                  "switch type": "linear",
                  "backlight": "white",
                  "size": "full size"
                },
                "available": false,
                "price": 249.95
              },
              "4402162122": {
                "item_id": "4402162122",
                "options": {
                  "switch type": "tactile",
                  "backlight": "RGB",
                  "size": "60%"
                },
                "available": true,
                "price": 233.9
              },
              "1151293680": {
                "item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": true,
                "price": 272.33
              },
              "2299424241": {
                "item_id": "2299424241",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "80%"
                },
                "available": true,
                "price": 237.48
              },
              "4843487907": {
                "item_id": "4843487907",
                "options": {
                  "switch type": "clicky",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": false,
                "price": 254.84
              },
              "9025753381": {
                "item_id": "9025753381",
                "options": {
                  "switch type": "clicky",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "available": false,
                "price": 231.58
              },
              "6439196450": {
                "item_id": "6439196450",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "60%"
                },
                "available": false,
                "price": 254.56
              },
              "9991484137": {
                "item_id": "9991484137",
                "options": {
                  "switch type": "tactile",
                  "backlight": "white",
                  "size": "80%"
                },
                "available": true,
                "price": 240.97
              },
              "9665000388": {
                "item_id": "9665000388",
                "options": {
                  "switch type": "clicky",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 269.46
              },
              "9570044148": {
                "item_id": "9570044148",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "full size"
                },
                "available": true,
                "price": 231.37
              },
              "7658724607": {
                "item_id": "7658724607",
                "options": {
                  "switch type": "tactile",
                  "backlight": "none",
                  "size": "80%"
                },
                "available": true,
                "price": 256.73
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            8
          ]
        },
        "catalog:4896585277": {
          "value": {
            "name": "Smart Thermostat",
            "product_id": "4896585277",
            "variants": {
              "8722653925": {
                "item_id": "8722653925",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "white"
                },
                "available": false,
                "price": 227.8
              },
              "8593894906": {
                "item_id": "8593894906",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "white"
                },
                "available": false,
                "price": 263.11
              },
              "2791467853": {
                "item_id": "2791467853",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "stainless steel"
                },
                "available": false,
                "price": 242.53
              },
              "7747408585": {
                "item_id": "7747408585",
                "options": {
                  "compatibility": "Google Assistant",
                  "color": "black"
                },
                "available": true,
                "price": 249.01
              },
              "4953074738": {
                "item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "available": true,
                "price": 226.02
              },
              "4983901480": {
                "item_id": "4983901480",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "black"
                },
                "available": true,
                "price": 262.47
              },
              "9480266227": {
                "item_id": "9480266227",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 255.98
              },
              "6243148452": {
                "item_id": "6243148452",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "stainless steel"
                },
                "available": true,
                "price": 247.0
              },
              "3377900078": {
                "item_id": "3377900078",
                "options": {
                  "compatibility": "Apple HomeKit",
                  "color": "white"
                },
                "available": true,
                "price": 260.68
              }
            }
          },
          "version": 1,
          "status": "supported",
          "depends_on": [],
          "sources": [
            10
          ]
        },
        "match:4983901480": {
          "value": [
            "4953074738"
          ],
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4983901480",
            "catalog:4896585277",
            "order:#W1483350"
          ],
          "sources": [
            10,
            12
          ]
        },
        "delta:4983901480": {
          "value": -36.45,
          "version": 1,
          "status": "supported",
          "depends_on": [
            "match:4983901480",
            "catalog:4896585277"
          ],
          "sources": [
            10
          ]
        },
        "match:9570044148": {
          "value": [
            "1421289881"
          ],
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:9570044148",
            "catalog:1656367028",
            "order:#W1483350"
          ],
          "sources": [
            8,
            16
          ]
        },
        "delta:9570044148": {
          "value": 37.4,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "match:9570044148",
            "catalog:1656367028"
          ],
          "sources": [
            8
          ]
        },
        "total": {
          "value": 0.95,
          "version": 2,
          "status": "supported",
          "depends_on": [
            "delta:9570044148",
            "delta:4983901480"
          ],
          "sources": [
            17
          ]
        },
        "confirmation:4983901480": {
          "value": "3ba8b2d04fbd21b430ac",
          "version": 1,
          "status": "supported",
          "depends_on": [
            "requirement:4983901480",
            "match:4983901480",
            "delta:4983901480"
          ],
          "sources": [
            14,
            15
          ]
        },
        "confirmation:9570044148": {
          "value": "f3810cf4150ba8eba6bf",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "requirement:9570044148",
            "match:9570044148",
            "delta:9570044148"
          ],
          "sources": [
            19,
            20
          ]
        },
        "authorization": {
          "value": "1aeb3d51ffd6200fc779",
          "version": 2,
          "status": "supported",
          "depends_on": [
            "scope",
            "payment",
            "total",
            "confirmation:9570044148",
            "confirmation:4983901480"
          ],
          "sources": [
            19,
            20
          ]
        }
      },
      "product_refs": {
        "1656367028": 8,
        "4896585277": 10
      },
      "orders": {
        "#W1483350": {
          "order_id": "#W1483350",
          "user_id": "noah_khan_5763",
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "items": [
            {
              "name": "Mechanical Keyboard",
              "product_id": "1656367028",
              "item_id": "9570044148",
              "price": 231.37,
              "options": {
                "switch type": "linear",
                "backlight": "none",
                "size": "full size"
              }
            },
            {
              "name": "Smart Thermostat",
              "product_id": "4896585277",
              "item_id": "4983901480",
              "price": 262.47,
              "options": {
                "compatibility": "Apple HomeKit",
                "color": "black"
              }
            },
            {
              "name": "Digital Camera",
              "product_id": "8940227892",
              "item_id": "4326528037",
              "price": 2714.51,
              "options": {
                "resolution": "24MP",
                "zoom": "5x",
                "storage": "CF card"
              }
            },
            {
              "name": "Cycling Helmet",
              "product_id": "7765186836",
              "item_id": "6697922351",
              "price": 194.47,
              "options": {
                "size": "L",
                "color": "white",
                "ventilation": "medium"
              }
            },
            {
              "name": "Smart Watch",
              "product_id": "6945232052",
              "item_id": "9320099340",
              "price": 375.03,
              "options": {
                "color": "black",
                "band material": "leather",
                "display": "AMOLED"
              }
            }
          ],
          "status": "delivered",
          "fulfillments": [
            {
              "tracking_id": [
                "151624030573"
              ],
              "item_ids": [
                "9570044148",
                "4983901480",
                "4326528037",
                "6697922351",
                "9320099340"
              ]
            }
          ],
          "payment_history": [
            {
              "transaction_type": "payment",
              "amount": 3777.85,
              "payment_method_id": "paypal_2319812"
            }
          ],
          "cancel_reason": null,
          "exchange_items": null,
          "exchange_new_items": null,
          "exchange_payment_method_id": null,
          "exchange_price_difference": null,
          "return_items": null,
          "return_payment_method_id": null
        }
      },
      "users": {
        "noah_khan_5763": {
          "user_id": "noah_khan_5763",
          "name": {
            "first_name": "Noah",
            "last_name": "Khan"
          },
          "address": {
            "address1": "143 Highland Drive",
            "address2": "Suite 928",
            "city": "San Francisco",
            "country": "USA",
            "state": "CA",
            "zip": "94140"
          },
          "email": "noah.khan7453@example.com",
          "payment_methods": {
            "paypal_2319812": {
              "source": "paypal",
              "id": "paypal_2319812"
            }
          },
          "orders": [
            "#W1483350",
            "#W3818056"
          ]
        }
      },
      "evidence": {},
      "authenticated": "noah_khan_5763",
      "scope": [
        "9570044148",
        "4983901480"
      ],
      "requirements": {
        "9570044148": {
          "switch type": "linear",
          "backlight": "none",
          "size": "80%"
        },
        "4983901480": {
          "compatibility": "Amazon Alexa",
          "color": "black"
        }
      },
      "old_confirmations": [
        {
          "fingerprint": "1aeb3d51ffd6200fc779",
          "user_ref": 20,
          "assistant_ref": 19,
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1421289881",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "difference": 0.95
        }
      ],
      "proposals": [
        {
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1151293680",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4983901480",
                "new_item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "new_price": 226.02,
                "old_price": 262.47,
                "difference": -36.45,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "9570044148",
                "new_item_id": "1151293680",
                "options": {
                  "switch type": "linear",
                  "backlight": "RGB",
                  "size": "full size"
                },
                "new_price": 272.33,
                "old_price": 231.37,
                "difference": 40.96,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 4.51,
            "fingerprint": "36b73193e480e4038297",
            "order_id": "#W1483350",
            "payment_method_id": "paypal_2319812",
            "pairs": [
              [
                "4983901480",
                "4953074738"
              ],
              [
                "9570044148",
                "1151293680"
              ]
            ]
          },
          "source": 12
        },
        {
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1421289881",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4983901480",
                "new_item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "new_price": 226.02,
                "old_price": 262.47,
                "difference": -36.45,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "9570044148",
                "new_item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "new_price": 268.77,
                "old_price": 231.37,
                "difference": 37.4,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 0.95,
            "fingerprint": "1aeb3d51ffd6200fc779",
            "order_id": "#W1483350",
            "payment_method_id": "paypal_2319812",
            "pairs": [
              [
                "4983901480",
                "4953074738"
              ],
              [
                "9570044148",
                "1421289881"
              ]
            ]
          },
          "source": 17
        },
        {
          "arguments": {
            "order_id": "#W1483350",
            "item_ids": [
              "9570044148",
              "4983901480"
            ],
            "new_item_ids": [
              "1421289881",
              "4953074738"
            ],
            "payment_method_id": "paypal_2319812"
          },
          "plan": {
            "rows": [
              {
                "item_id": "4983901480",
                "new_item_id": "4953074738",
                "options": {
                  "compatibility": "Amazon Alexa",
                  "color": "black"
                },
                "new_price": 226.02,
                "old_price": 262.47,
                "difference": -36.45,
                "sources": [
                  10
                ]
              },
              {
                "item_id": "9570044148",
                "new_item_id": "1421289881",
                "options": {
                  "switch type": "linear",
                  "backlight": "none",
                  "size": "80%"
                },
                "new_price": 268.77,
                "old_price": 231.37,
                "difference": 37.4,
                "sources": [
                  8
                ]
              }
            ],
            "difference": 0.95,
            "fingerprint": "1aeb3d51ffd6200fc779",
            "order_id": "#W1483350",
            "payment_method_id": "paypal_2319812",
            "pairs": [
              [
                "4983901480",
                "4953074738"
              ],
              [
                "9570044148",
                "1421289881"
              ]
            ]
          },
          "source": 19
        }
      ],
      "events": [],
      "work_log": [],
      "order_id": "#W1483350",
      "payment": "paypal_2319812",
      "completed_writes": 0,
      "review_audit": [
        {
          "item_ids": [
            "4983901480"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:4983901480"
          ]
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 12,
          "changed_record_keys": [
            "match:9570044148"
          ]
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 16,
          "changed_record_keys": [
            "match:9570044148"
          ]
        },
        {
          "item_ids": [
            "4983901480"
          ],
          "source": 17,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 17,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "4983901480"
          ],
          "source": 19,
          "changed_record_keys": []
        },
        {
          "item_ids": [
            "9570044148"
          ],
          "source": 19,
          "changed_record_keys": []
        }
      ]
    }
  }
}
```
首个后续工作：`{"event":6,"object":"#W1483350","parameters":{},"reason":"Every current item is specified and in stock, and the whole amount is within the cap.","source":"program","work_type":"prepare"}`

