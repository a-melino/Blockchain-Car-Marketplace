// SPDX-License-Identifier: MIT
pragma experimental ABIEncoderV2;
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract CarMarketplace is ERC721Full {

    constructor() public ERC721Full("CarToken", "CAR") {}

    struct Car {
        string brand;
        string model;
        uint256 year;
        uint256 kilometers;
        string fuelType;
        string engine;
        string transmission;
        uint256 accident;
        uint256 cleanTitle;
        uint256 price;
        bool isForSale;
        string carJson;
    }

    mapping (uint256 => Car) public carCollection;

    function getCarDetails(uint256 tokenId) public view returns (string memory detailsJson) {
        return carCollection[tokenId].carJson;
    }

    function registerCar(
        address ownerAddress, 
        Car memory newCar,
        string memory carURI
    ) public returns (uint256) {

        uint256 tokenId = totalSupply();
        _mint(ownerAddress, tokenId);
        _setTokenURI(tokenId, carURI);

        carCollection[tokenId] = newCar;

        return tokenId;
    }


    // function buyCar (address owner, string memory tokenURI) public returns (uint256) { }

    // function rentCar (address owner, string memory tokenURI) public returns (uint256) { }

}
