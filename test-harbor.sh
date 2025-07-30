#!/bin/bash

# Harbor连接测试脚本

REGISTRY="harbor.5845.cn"
PROJECT="myapi"

echo "🔍 测试Harbor连接..."

# 测试网络连接
echo "1. 测试网络连接..."
curl -I http://$REGISTRY && echo "✅ HTTP连接正常" || echo "❌ HTTP连接失败"
curl -I https://$REGISTRY && echo "✅ HTTPS连接正常" || echo "❌ HTTPS连接失败（证书问题）"

# 测试DNS解析
echo "2. 测试DNS解析..."
nslookup $REGISTRY && echo "✅ DNS解析正常" || echo "❌ DNS解析失败"

# 测试harbor.local解析
echo "3. 测试harbor.local解析..."
nslookup harbor.local && echo "✅ harbor.local解析正常" || echo "❌ harbor.local解析失败"

# 添加hosts配置
echo "4. 添加hosts配置..."
HARBOR_IP=$(dig +short $REGISTRY | head -1)
if [ ! -z "$HARBOR_IP" ]; then
    echo "Harbor IP: $HARBOR_IP"
    echo "$HARBOR_IP harbor.local" | sudo tee -a /etc/hosts
    echo "✅ hosts配置已添加"
else
    echo "❌ 无法获取Harbor IP"
fi

echo "5. 测试Docker登录..."
echo "请提供Harbor用户名和密码进行测试"
echo "使用方法: ./test-harbor.sh username password"

if [ $# -eq 2 ]; then
    USERNAME=$1
    PASSWORD=$2
    
    echo "尝试登录Harbor..."
    echo $PASSWORD | docker login $REGISTRY -u $USERNAME --password-stdin && {
        echo "✅ Harbor登录成功！"
        
        echo "6. 测试镜像构建和推送..."
        docker build -t $REGISTRY/$PROJECT/myapi:test .
        
        echo "7. 推送测试镜像..."
        docker push $REGISTRY/$PROJECT/myapi:test && {
            echo "✅ 镜像推送成功！"
            
            echo "8. 清理测试镜像..."
            docker rmi $REGISTRY/$PROJECT/myapi:test
            echo "✅ 测试完成！"
        } || {
            echo "❌ 镜像推送失败"
            docker rmi $REGISTRY/$PROJECT/myapi:test
        }
    } || {
        echo "❌ Harbor登录失败"
        echo "尝试HTTP登录..."
        echo $PASSWORD | docker login http://$REGISTRY -u $USERNAME --password-stdin && {
            echo "✅ HTTP登录成功！"
        } || {
            echo "❌ HTTP登录也失败"
        }
    }
else
    echo "请提供用户名和密码参数"
    echo "示例: ./test-harbor.sh admin password"
fi 