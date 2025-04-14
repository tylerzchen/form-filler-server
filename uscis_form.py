send_raw_email
SES.Client.send_raw_email(**kwargs)
Composes an email message and immediately queues it for sending.

This operation is more flexible than the SendEmail operation. When you use the SendRawEmail operation, you can specify the headers of the message as well as its content. This flexibility is useful, for example, when you need to send a multipart MIME email (such a message that contains both a text and an HTML version). You can also use this operation to send messages that include attachments.

The SendRawEmail operation has the following requirements:

You can only send email from verified email addresses or domains. If you try to send email from an address that isn’t verified, the operation results in an “Email address not verified” error.

If your account is still in the Amazon SES sandbox, you can only send email to other verified addresses in your account, or to addresses that are associated with the Amazon SES mailbox simulator.

The maximum message size, including attachments, is 10 MB.

Each message has to include at least one recipient address. A recipient address includes any address on the To:, CC:, or BCC: lines.

If you send a single message to more than one recipient address, and one of the recipient addresses isn’t in a valid format (that is, it’s not in the format UserName@[SubDomain.]Domain.TopLevelDomain), Amazon SES rejects the entire message, even if the other addresses are valid.

Each message can include up to 50 recipient addresses across the To:, CC:, or BCC: lines. If you need to send a single message to more than 50 recipients, you have to split the list of recipient addresses into groups of less than 50 recipients, and send separate messages to each group.

Amazon SES allows you to specify 8-bit Content-Transfer-Encoding for MIME message parts. However, if Amazon SES has to modify the contents of your message (for example, if you use open and click tracking), 8-bit content isn’t preserved. For this reason, we highly recommend that you encode all content that isn’t 7-bit ASCII. For more information, see MIME Encoding in the Amazon SES Developer Guide.

Additionally, keep the following considerations in mind when using the SendRawEmail operation:

Although you can customize the message headers when using the SendRawEmail operation, Amazon SES automatically applies its own Message-ID and Date headers; if you passed these headers when creating the message, they are overwritten by the values that Amazon SES provides.

If you are using sending authorization to send on behalf of another user, SendRawEmail enables you to specify the cross-account identity for the email’s Source, From, and Return-Path parameters in one of two ways: you can pass optional parameters SourceArn, FromArn, and/or ReturnPathArn, or you can include the following X-headers in the header of your raw email:

X-SES-SOURCE-ARN

X-SES-FROM-ARN

X-SES-RETURN-PATH-ARN

Warning
Don’t include these X-headers in the DKIM signature. Amazon SES removes these before it sends the email.

If you only specify the SourceIdentityArn parameter, Amazon SES sets the From and Return-Path addresses to the same identity that you specified.

For more information about sending authorization, see the Using Sending Authorization with Amazon SES in the Amazon SES Developer Guide.

For every message that you send, the total number of recipients (including each recipient in the To:, CC: and BCC: fields) is counted against the maximum number of emails you can send in a 24-hour period (your sending quota). For more information about sending quotas in Amazon SES, see Managing Your Amazon SES Sending Limits in the Amazon SES Developer Guide.

See also: AWS API Documentation

Request Syntax
response = client.send_raw_email(
    Source='string',
    Destinations=[
        'string',
    ],
    RawMessage={
        'Data': b'bytes'
    },
    FromArn='string',
    SourceArn='string',
    ReturnPathArn='string',
    Tags=[
        {
            'Name': 'string',
            'Value': 'string'
        },
    ],
    ConfigurationSetName='string'
)
Parameters:
Source (string) –

The identity’s email address. If you do not provide a value for this parameter, you must specify a “From” address in the raw text of the message. (You can also specify both.)

Note
Amazon SES does not support the SMTPUTF8 extension, as described in RFC6531. For this reason, the email address string must be 7-bit ASCII. If you want to send to or from email addresses that contain Unicode characters in the domain part of an address, you must encode the domain using Punycode. Punycode is not permitted in the local part of the email address (the part before the @ sign) nor in the “friendly from” name. If you want to use Unicode characters in the “friendly from” name, you must encode the “friendly from” name using MIME encoded-word syntax, as described in Sending raw email using the Amazon SES API. For more information about Punycode, see RFC 3492.

If you specify the Source parameter and have feedback forwarding enabled, then bounces and complaints are sent to this email address. This takes precedence over any Return-Path header that you might include in the raw text of the message.

Destinations (list) –

A list of destinations for the message, consisting of To:, CC:, and BCC: addresses.

(string) –

RawMessage (dict) –

[REQUIRED]

The raw email message itself. The message has to meet the following criteria:

The message has to contain a header and a body, separated by a blank line.

All of the required header fields must be present in the message.

Each part of a multipart MIME message must be formatted properly.

Attachments must be of a content type that Amazon SES supports. For a list on unsupported content types, see Unsupported Attachment Types in the Amazon SES Developer Guide.

The entire message must be base64-encoded.

If any of the MIME parts in your message contain content that is outside of the 7-bit ASCII character range, we highly recommend that you encode that content. For more information, see Sending Raw Email in the Amazon SES Developer Guide.

Per RFC 5321, the maximum length of each line of text, including the <CRLF>, must not exceed 1,000 characters.

Data (bytes) – [REQUIRED]

The raw data of the message. This data needs to base64-encoded if you are accessing Amazon SES directly through the HTTPS interface. If you are accessing Amazon SES using an Amazon Web Services SDK, the SDK takes care of the base 64-encoding for you. In all cases, the client must ensure that the message format complies with Internet email standards regarding email header fields, MIME types, and MIME encoding.

The To:, CC:, and BCC: headers in the raw message can contain a group list.

If you are using SendRawEmail with sending authorization, you can include X-headers in the raw message to specify the “Source,” “From,” and “Return-Path” addresses. For more information, see the documentation for SendRawEmail.

Warning
Do not include these X-headers in the DKIM signature, because they are removed by Amazon SES before sending the email.

For more information, go to the Amazon SES Developer Guide.

FromArn (string) –

This parameter is used only for sending authorization. It is the ARN of the identity that is associated with the sending authorization policy that permits you to specify a particular “From” address in the header of the raw email.

Instead of using this parameter, you can use the X-header X-SES-FROM-ARN in the raw message of the email. If you use both the FromArn parameter and the corresponding X-header, Amazon SES uses the value of the FromArn parameter.

Note
For information about when to use this parameter, see the description of SendRawEmail in this guide, or see the Amazon SES Developer Guide.

SourceArn (string) –

This parameter is used only for sending authorization. It is the ARN of the identity that is associated with the sending authorization policy that permits you to send for the email address specified in the Source parameter.

For example, if the owner of example.com (which has ARN arn:aws:ses:us-east-1:123456789012:identity/example.com) attaches a policy to it that authorizes you to send from user@example.com, then you would specify the SourceArn to be arn:aws:ses:us-east-1:123456789012:identity/example.com, and the Source to be user@example.com.

Instead of using this parameter, you can use the X-header X-SES-SOURCE-ARN in the raw message of the email. If you use both the SourceArn parameter and the corresponding X-header, Amazon SES uses the value of the SourceArn parameter.

Note
For information about when to use this parameter, see the description of SendRawEmail in this guide, or see the Amazon SES Developer Guide.

ReturnPathArn (string) –

This parameter is used only for sending authorization. It is the ARN of the identity that is associated with the sending authorization policy that permits you to use the email address specified in the ReturnPath parameter.

For example, if the owner of example.com (which has ARN arn:aws:ses:us-east-1:123456789012:identity/example.com) attaches a policy to it that authorizes you to use feedback@example.com, then you would specify the ReturnPathArn to be arn:aws:ses:us-east-1:123456789012:identity/example.com, and the ReturnPath to be feedback@example.com.

Instead of using this parameter, you can use the X-header X-SES-RETURN-PATH-ARN in the raw message of the email. If you use both the ReturnPathArn parameter and the corresponding X-header, Amazon SES uses the value of the ReturnPathArn parameter.

Note
For information about when to use this parameter, see the description of SendRawEmail in this guide, or see the Amazon SES Developer Guide.

Tags (list) –

A list of tags, in the form of name/value pairs, to apply to an email that you send using SendRawEmail. Tags correspond to characteristics of the email that you define, so that you can publish email sending events.

(dict) –

Contains the name and value of a tag that you can provide to SendEmail or SendRawEmail to apply to an email.

Message tags, which you use with configuration sets, enable you to publish email sending events. For information about using configuration sets, see the Amazon SES Developer Guide.

Name (string) – [REQUIRED]

The name of the tag. The name must meet the following requirements:

Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).

Contain 256 characters or fewer.

Value (string) – [REQUIRED]

The value of the tag. The value must meet the following requirements:

Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).

Contain 256 characters or fewer.

ConfigurationSetName (string) – The name of the configuration set to use when you send an email using SendRawEmail.

Return type:
dict

Returns:
Response Syntax
{
    'MessageId': 'string'
}
Response Structure
(dict) –

Represents a unique message ID.

MessageId (string) –

The unique message identifier returned from the SendRawEmail action.

Exceptions
SES.Client.exceptions.MessageRejected

SES.Client.exceptions.MailFromDomainNotVerifiedException

SES.Client.exceptions.ConfigurationSetDoesNotExistException

SES.Client.exceptions.ConfigurationSetSendingPausedException

SES.Client.exceptions.AccountSendingPausedException

Examples
The following example sends an email with an attachment:

response = client.send_raw_email(
    Destinations=[
    ],
    FromArn='',
    RawMessage={
        'Data': 'From: sender@example.com\nTo: recipient@example.com\nSubject: Test email (contains an attachment)\nMIME-Version: 1.0\nContent-type: Multipart/Mixed; boundary="NextPart"\n\n--NextPart\nContent-Type: text/plain\n\nThis is the message body.\n\n--NextPart\nContent-Type: text/plain;\nContent-Disposition: attachment; filename="attachment.txt"\n\nThis is the text in the attachment.\n\n--NextPart--',
    },
    ReturnPathArn='',
    Source='',
    SourceArn='',
)

print(response)
Expected Output:

{
    'MessageId': 'EXAMPLEf3f73d99b-c63fb06f-d263-41f8-a0fb-d0dc67d56c07-000000',
    'ResponseMetadata': {
        '...': '...',
    },
}
