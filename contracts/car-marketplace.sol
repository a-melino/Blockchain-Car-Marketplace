// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract CarMarketplace is ERC721Full {

    constructor() public ERC721Full("CarToken", "CAR") {}

    struct Car {
        string brand;
        string model;
        uint256 year;
        uint256 mileage;
        bool accident;
        string carJson;
    }

    mapping (uint256 => Car) public carCollection;

    event Appraisal(uint256 tokenID, uint newAppraisalValue, string reportURI, string propertyJson);

    function getCarDetails(uint256 tokenId) public view returns (string memory detailsJson) {
        return carCollection[tokenId].carJson;
    }

    function registerCar(
        address ownerAddress, 
        string memory brand,
        string memory model,
        uint256 year,
        uint256 mileage,
        bool accident,
        string memory carJson,
        string memory tokenURI
    ) public returns (uint256) {

        uint256 tokenId = totalSupply();
        _mint(ownerAddress, tokenId);
        _setTokenURI(tokenId, tokenURI);

        carCollection[tokenId] = Car(brand, model, year, mileage, accident, carJson);

        return tokenId;
    }


    // function buyCar (address owner, string memory tokenURI) public returns (uint256) { }

    // function rentCar (address owner, string memory tokenURI) public returns (uint256) { }

}
