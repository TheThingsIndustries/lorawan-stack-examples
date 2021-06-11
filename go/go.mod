module github.com/TheThingsIndustries/lorawan-stack-examples/go

go 1.16

replace gopkg.in/DATA-DOG/go-sqlmock.v1 => gopkg.in/DATA-DOG/go-sqlmock.v1 v1.3.0

replace gocloud.dev => gocloud.dev v0.19.0

replace github.com/grpc-ecosystem/grpc-gateway => github.com/TheThingsIndustries/grpc-gateway v1.15.2-gogo

require (
	github.com/gogo/protobuf v1.3.2
	go.thethings.network/lorawan-stack/v3 v3.13.0
	google.golang.org/grpc v1.37.0
)
